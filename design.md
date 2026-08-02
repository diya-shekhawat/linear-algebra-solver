# Algebrify Design System
## Yellow · White · Black Theme

### Color Palette

| Token | Value | Usage |
|---|---|---|
| `--yellow` | `#FFD600` | Primary accent, CTA buttons, highlights |
| `--yellow-dark` | `#F5C000` | Hover states, borders |
| `--yellow-light` | `#FFFBE6` | Tinted backgrounds, cards |
| `--black` | `#0A0A0A` | Primary text, hero bg |
| `--black-mid` | `#1A1A1A` | Navbar, sidebar bg |
| `--black-card` | `#212121` | Dark cards |
| `--white` | `#FFFFFF` | Main content background |
| `--white-off` | `#F9F9F9` | Subtle alternation |
| `--gray` | `#555555` | Muted text |
| `--gray-lt` | `#E8E8E8` | Borders |

### Layout — Solver Pages

```
NAVBAR (black bg, yellow brand accent)
LEFT SIDEBAR (black, 320px) | MAIN CONTENT (white)
 - Tool selector             | - Step-by-step solution
 - Input grids               | - Final result box
 - Matrix cells              | - Step cards (yellow border)
 - Solve button              | - Formula chips (black+yellow)
 - Formula ref               | - Explanations
 - All calculations here     |
```

### Typography
- Headings: Space Grotesk bold
- Body: Inter
- Math cells: JetBrains Mono
- Accent: Playfair Display Italic (hero only)

### Components
- Sidebar: black bg, white text, yellow labels
- Solve Button: yellow bg, black bold text, hover glow
- Step Cards: yellow left border, pale yellow bg
- Formula Chip: black bg, yellow mono text
- Result Box: black bg, yellow border + text
- Navbar: black bg, yellow active underline
