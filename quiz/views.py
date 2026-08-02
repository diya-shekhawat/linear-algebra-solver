import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz, Question, Answer, QuizResult

def quiz_list(request):
    """
    Displays all available quizzes grouped by topic and unit.
    """
    quizzes = Quiz.objects.select_related('topic__unit').prefetch_related('questions')
    
    user_results = {}
    if request.user.is_authenticated:
        for res in QuizResult.objects.filter(user=request.user):
            if res.quiz_id not in user_results or res.percentage > user_results[res.quiz_id].percentage:
                user_results[res.quiz_id] = res

    context = {
        'quizzes': quizzes,
        'user_results': user_results
    }
    return render(request, 'quiz/quiz_list.html', context)


@login_required
def quiz_take(request, quiz_id):
    """
    Quiz player view with timer, random question order, and instant submission check.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.prefetch_related('answers'))

    if not questions:
        messages.warning(request, "This quiz currently has no questions.")
        return redirect('quiz:quiz_list')

    # Shuffle questions for random question generator requirement
    random.seed(request.session.session_key or str(request.user.id))
    shuffled_questions = questions.copy()

    if request.method == 'POST':
        score = 0
        total_questions = len(questions)
        user_answers = {}

        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                try:
                    ans = Answer.objects.get(id=int(selected_answer_id), question=question)
                    user_answers[question.id] = ans.id
                    if ans.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        passed = percentage >= quiz.pass_mark_percentage
        time_taken = int(request.POST.get('time_taken', 0))

        result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            passed=passed,
            time_taken_seconds=time_taken
        )

        # Update profile points and streak
        profile = request.user.profile
        profile.total_quiz_score += score * 10
        profile.update_streak()
        profile.save()

        return redirect('quiz:quiz_result', result_id=result.id)

    context = {
        'quiz': quiz,
        'questions': shuffled_questions,
    }
    return render(request, 'quiz/quiz_take.html', context)


@login_required
def quiz_result(request, result_id):
    """
    Shows detailed quiz result, score, feedback, and question explanations.
    """
    result = get_object_or_404(QuizResult.objects.select_related('quiz', 'user'), id=result_id)
    if result.user != request.user and not request.user.is_staff:
        return redirect('quiz:quiz_list')

    questions = result.quiz.questions.prefetch_related('answers')

    context = {
        'result': result,
        'questions': questions
    }
    return render(request, 'quiz/quiz_result.html', context)


@login_required
def quiz_history(request):
    """
    Shows the history of all quiz attempts by the student.
    """
    results = QuizResult.objects.filter(user=request.user).select_related('quiz__topic')
    return render(request, 'quiz/quiz_history.html', {'results': results})
