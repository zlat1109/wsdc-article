---
name: web-development
description: Creates and maintains web interfaces using HTML, CSS, and JavaScript. Implements responsive design, accessibility standards, and modern web practices. Use when working with HTML files, CSS styling, JavaScript functionality, or web interface development.
---

# Web Development

## Quick Start

When developing web interfaces:

1. Create semantic HTML structure
2. Implement responsive CSS styling
3. Add JavaScript functionality
4. Ensure accessibility
5. Test across browsers
6. Optimize performance

## HTML Development

### Semantic HTML5

- Use semantic elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`)
- Implement proper document structure
- Use appropriate heading hierarchy (h1 → h2 → h3)
- Provide alt text for images
- Use meaningful element names

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Page description">
    <title>Page Title</title>
</head>
<body>
    <header>
        <nav>
            <!-- Navigation -->
        </nav>
    </header>
    <main>
        <article>
            <!-- Main content -->
        </article>
    </main>
    <footer>
        <!-- Footer -->
    </footer>
</body>
</html>
```

### Accessibility (A11y)

- Implement ARIA attributes where needed
- Ensure keyboard navigation
- Provide screen reader support
- Test with assistive technologies
- Maintain proper color contrast (WCAG AA minimum)

**ARIA Examples:**
```html
<button aria-label="Close menu" aria-expanded="false">
    <span aria-hidden="true">×</span>
</button>

<form>
    <label for="email">Email</label>
    <input 
        type="email" 
        id="email" 
        name="email" 
        required 
        aria-describedby="email-error"
        aria-invalid="false"
    >
    <span id="email-error" role="alert" aria-live="polite"></span>
</form>
```

## CSS Development

### Responsive Design

- Use mobile-first approach
- Implement flexible grid systems
- Use CSS custom properties (variables)
- Implement media queries appropriately
- Test on different screen sizes

**Mobile-First Example:**
```css
/* Base styles (mobile) */
.container {
    padding: 1rem;
    width: 100%;
}

/* Tablet and up */
@media (min-width: 768px) {
    .container {
        padding: 2rem;
        max-width: 750px;
        margin: 0 auto;
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .container {
        max-width: 980px;
        padding: 3rem;
    }
}
```

### CSS Architecture

- Use BEM methodology for naming
- Organize styles logically
- Use CSS custom properties for theming
- Avoid deep nesting (max 3 levels)
- Keep specificity low

**BEM Naming:**
```css
/* Block */
.nav {}

/* Element */
.nav__item {}
.nav__link {}

/* Modifier */
.nav__item--active {}
.nav--vertical {}
```

**CSS Custom Properties:**
```css
:root {
    --primary-color: #2d3748;
    --secondary-color: #4a5568;
    --spacing-unit: 1rem;
    --border-radius: 4px;
}

.button {
    background-color: var(--primary-color);
    padding: var(--spacing-unit);
    border-radius: var(--border-radius);
}
```

### Performance

- Minimize CSS file size
- Use efficient selectors
- Avoid expensive properties (box-shadow, filter) in animations
- Use CSS transforms for animations
- Implement critical CSS inline

**Efficient Animations:**
```css
/* ✅ GOOD - Uses transform (GPU accelerated) */
.element {
    transition: transform 0.3s ease;
}
.element:hover {
    transform: translateY(-5px);
}

/* ❌ BAD - Uses top/left (layout recalculation) */
.element {
    transition: top 0.3s ease;
}
.element:hover {
    top: -5px;
}
```

## JavaScript Development

### Modern JavaScript

- Use ES6+ features
- Implement proper error handling
- Use async/await for asynchronous code
- Follow functional programming principles
- Avoid global variables

**Error Handling:**
```javascript
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        // Handle error gracefully
        return null;
    }
}
```

### Best Practices

- Use meaningful variable names
- Implement proper error boundaries
- Handle errors gracefully
- Use event delegation for dynamic content
- Optimize DOM manipulation

**Event Delegation:**
```javascript
// ✅ GOOD - Event delegation
document.addEventListener('click', (e) => {
    if (e.target.matches('.button')) {
        handleButtonClick(e.target);
    }
});

// ❌ BAD - Direct event listeners on dynamic elements
document.querySelectorAll('.button').forEach(btn => {
    btn.addEventListener('click', handleButtonClick);
});
```

## Performance Optimization

### Code Optimization

- Minimize bundle size
- Use code splitting for large apps
- Implement lazy loading for images
- Optimize images (WebP format, appropriate sizes)
- Use efficient algorithms

**Image Optimization:**
```html
<!-- Responsive images -->
<img 
    srcset="image-320w.webp 320w,
            image-640w.webp 640w,
            image-1024w.webp 1024w"
    sizes="(max-width: 640px) 100vw,
           (max-width: 1024px) 50vw,
           33vw"
    src="image-640w.webp"
    alt="Description"
    loading="lazy"
>
```

### Browser Optimization

- Use CDN for assets when possible
- Implement proper caching headers
- Minimize HTTP requests
- Use compression (gzip, brotli)
- Optimize font loading

**Font Loading:**
```html
<!-- Preload critical fonts -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>

<!-- Use font-display for better performance -->
<style>
@font-face {
    font-family: 'Custom Font';
    src: url('font.woff2') format('woff2');
    font-display: swap; /* Shows fallback immediately */
}
</style>
```

## Testing

### Browser Testing

- Test in Chrome, Firefox, Safari, Edge
- Test on mobile devices
- Use browser dev tools
- Test with different screen sizes
- Check accessibility with Lighthouse

### Tools

- **Lighthouse** - Performance and accessibility
- **WAVE** - Accessibility testing
- **PageSpeed Insights** - Performance analysis
- **BrowserStack** - Cross-browser testing (if needed)

**Lighthouse Checklist:**
- Performance score > 90
- Accessibility score > 90
- Best Practices score > 90
- SEO score > 90

## Common Patterns

### Responsive Navigation

```html
<nav class="nav">
    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span aria-hidden="true">☰</span>
    </button>
    <ul class="nav-menu">
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
    </ul>
</nav>
```

```css
.nav-toggle {
    display: block;
}

.nav-menu {
    display: none;
}

.nav-menu.active {
    display: flex;
}

@media (min-width: 768px) {
    .nav-toggle {
        display: none;
    }
    .nav-menu {
        display: flex;
    }
}
```

### Accessible Forms

```html
<form>
    <div class="form-group">
        <label for="email">Email</label>
        <input 
            type="email" 
            id="email" 
            name="email" 
            required 
            aria-describedby="email-error email-help"
            aria-invalid="false"
        >
        <small id="email-help">We'll never share your email.</small>
        <span id="email-error" role="alert" aria-live="polite"></span>
    </div>
    
    <button type="submit">Submit</button>
</form>
```

```javascript
// Form validation
const form = document.querySelector('form');
const emailInput = document.getElementById('email');
const errorSpan = document.getElementById('email-error');

emailInput.addEventListener('blur', () => {
    if (!emailInput.validity.valid) {
        emailInput.setAttribute('aria-invalid', 'true');
        errorSpan.textContent = 'Please enter a valid email address.';
    } else {
        emailInput.setAttribute('aria-invalid', 'false');
        errorSpan.textContent = '';
    }
});
```

## Design Guidelines

Create distinctive, memorable designs that avoid generic "AI slop" aesthetics.

**Key principles:**
- Choose unique, characterful fonts (avoid Inter, Roboto, Arial)
- Commit to cohesive color schemes
- Use motion strategically
- Create unexpected layouts
- Add visual depth and texture

**See detailed guidelines:** [design-guidelines.md](reference/design-guidelines.md)

## Best Practices Summary

### Development
- Use semantic HTML
- Implement responsive design
- Ensure accessibility (WCAG AA)
- Optimize performance
- Test across browsers
- Document code
- **Create distinctive, memorable designs**

### Design
- Avoid generic "AI slop" aesthetics
- Choose distinctive typography
- Commit to cohesive color schemes
- Use motion strategically
- Create unexpected layouts
- Add visual depth and texture

### CURSOR IDE
- Use HTML/CSS/JS extensions
- Use browser dev tools
- Use Lighthouse for testing
- Follow coding standards
- Use IntelliSense effectively

### Security
- Validate all inputs
- Sanitize user data
- Use HTTPS
- Implement CSP headers
- Follow OWASP guidelines

### Performance
- Optimize images and assets
- Minimize HTTP requests
- Implement caching
- Use efficient CSS/JS
- Monitor performance metrics
