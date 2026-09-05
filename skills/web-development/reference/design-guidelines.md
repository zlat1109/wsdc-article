# Design Guidelines Reference

## Avoiding "AI Slop" Aesthetics

**NEVER use generic AI-generated aesthetics:**
- ❌ Overused fonts (Inter, Roboto, Arial, system fonts)
- ❌ Cliched color schemes (purple gradients on white backgrounds)
- ❌ Predictable layouts and component patterns
- ❌ Cookie-cutter design lacking character

**DO create distinctive designs:**
- ✅ Choose unique, characterful fonts
- ✅ Commit to bold aesthetic direction
- ✅ Use unexpected layouts and compositions
- ✅ Create memorable, context-specific designs

## Typography

**Choose distinctive fonts:**
- Avoid generic fonts (Arial, Inter, Roboto)
- Use unexpected, characterful font choices
- Pair distinctive display font with refined body font
- Consider context and audience

**Example:**
```css
/* ✅ GOOD - Distinctive font choice */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Crimson+Text:ital,wght@0,400;1,400&display=swap');

:root {
    --font-display: 'Space Grotesk', sans-serif;
    --font-body: 'Crimson Text', serif;
}

h1, h2, h3 {
    font-family: var(--font-display);
    font-weight: 700;
}

body {
    font-family: var(--font-body);
}
```

## Color & Theme

**Commit to cohesive aesthetic:**
- Use CSS variables for consistency
- Dominant colors with sharp accents outperform evenly-distributed palettes
- Match colors to aesthetic direction (minimalist, maximalist, retro, etc.)

**Example:**
```css
:root {
    /* Minimalist palette */
    --color-primary: #1a1a1a;
    --color-secondary: #f5f5f5;
    --color-accent: #0066cc;
    
    /* Or maximalist palette */
    --color-primary: #ff6b6b;
    --color-secondary: #4ecdc4;
    --color-accent: #ffe66d;
}
```

## Motion & Animations

**Use animations strategically:**
- Prioritize CSS-only solutions for HTML
- Focus on high-impact moments
- One well-orchestrated page load with staggered reveals creates more delight
- Use scroll-triggering and hover states that surprise

**Example:**
```css
/* Staggered reveal animation */
.reveal-item {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease forwards;
}

.reveal-item:nth-child(1) { animation-delay: 0.1s; }
.reveal-item:nth-child(2) { animation-delay: 0.2s; }
.reveal-item:nth-child(3) { animation-delay: 0.3s; }

@keyframes fadeInUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

## Spatial Composition

**Create unexpected layouts:**
- Asymmetry and overlap
- Diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density

**Example:**
```css
/* Asymmetric layout */
.container {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 2rem;
    align-items: start;
}

/* Overlap effect */
.card {
    margin-top: -2rem;
    position: relative;
    z-index: 1;
}
```

## Backgrounds & Visual Details

**Create atmosphere and depth:**
- Add contextual effects and textures
- Use gradient meshes, noise textures, geometric patterns
- Apply layered transparencies, dramatic shadows
- Custom decorative borders and grain overlays

**Example:**
```css
/* Texture overlay */
.background {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    position: relative;
}

.background::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('data:image/svg+xml;utf8,<svg>...</svg>');
    opacity: 0.1;
    pointer-events: none;
}
```
