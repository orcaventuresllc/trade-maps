# PRD – Contractor Insurance Metrics Map (Vanilla JS + Inline SVG)

## 1. Project Overview
We are building an **interactive US map** for our WordPress site (Kadence Theme + Blocks Pro) using:
- **Clean inline SVG** of all 50 states + D.C.
- **Vanilla JavaScript** (plain browser JS, no frameworks or libraries)
- **Four contractor insurance metrics**:
  1. **GL Premium as % Revenue (range)**
  2. **GL Savings as % of Premium (single %)**
  3. **GL Carrier Competitiveness** (percentile based on # of quotes relative to other states)
  4. **WC Rate per $100** (workers' comp cost per $100 of payroll)

The map will:
- Show hover tooltips and a state info card on desktop
- Replace the map with a dropdown on mobile
- Use **heatmap coloring** for each metric
- Require **no paid licenses**
- Be pasteable into a single **Kadence Custom HTML block**

---

## 2. Goals & Success Criteria

### Primary Goals
- Display all 50 states + D.C. with accurate boundaries
- Color states dynamically based on selected metric
- Allow instant toggling between the four metrics
- Provide a mobile-friendly dropdown fallback
- Keep implementation lightweight and free of licensing issues

### Success Criteria
- ✅ Four metric scenarios toggle smoothly
- ✅ Heatmap coloring recalculated per metric
- ✅ Desktop hover shows tooltip and updates info card
- ✅ Mobile dropdown provides equivalent functionality
- ✅ Code is self-contained (HTML + CSS + JS in one block)
- ✅ Works in modern browsers (Chrome, Safari, Firefox, Edge, iOS, Android)

---

## 3. Key Features

### 3.1 Map Display (Desktop)
- Inline SVG `<path>` elements for each state
- States identified by `id` or `data-code` attributes (e.g., `CA`, `TX`)
- Hover: state highlights + tooltip with metric value
- Click: updates info card with selected state's details

### 3.2 Mobile Fallback
- SVG map hidden under `768px` viewport
- `<select>` dropdown lists all states alphabetically
- Selecting a state updates the info card

### 3.3 Metric Toggle
Four toggle buttons allow switching datasets:
1. **GL Premium as % Revenue (range)**
   - Tooltip shows range string (e.g., `2.5% – 4.8%`)
   - Heatmap uses midpoint for coloring
2. **GL Savings as % of Premium (single %)**
   - Example: `18%`
   - Higher = better
3. **GL Carrier Competitiveness (percentile)**
   - Example: `92nd percentile`
   - Higher = better
4. **WC Rate per $100**
   - Example: `$4.50`
   - Lower = better (reverse heatmap scale)

### 3.4 Info Card
- State name
- Current metric label + value
- Subtext explanation of metric
- CTA link: "View insurance details for {State}"

---

## 4. Data Requirements

### Dataset Structure
Each metric stored as a JS object keyed by USPS code:

```javascript
const DATA = {
  glPremiumPct: {
    CA: { midpoint: 3.65, range: "2.5% – 4.8%" },
    TX: { midpoint: 4.20, range: "3.0% – 5.4%" },
    // ...
  },
  glSavingsPct: {
    CA: 18,
    TX: 15,
    // ...
  },
  glCompetitiveness: {
    CA: 92,
    TX: 87,
    // ...
  },
  wcRate: {
    CA: 4.50,
    TX: 3.90,
    // ...
  }
};
```

---

## 5. Technical Requirements

### Platform & Tools
- WordPress (Kadence Theme + Blocks Pro)
- Inline SVG of US map
- Vanilla JavaScript for interactivity
- Inline `<style>` scoped to container
- Inline `<script>` with datasets + logic

### Implementation Details
- JS applies colors by iterating SVG paths (`<path id="CA">`) and setting `fill` based on dataset values
- `mouseover` / `mouseout` events show tooltip
- `click` events update info card
- Toggle buttons (`data-metric`) change active dataset
- Mobile `<select>` replaces map and updates info card
- Heatmap:
  - Higher = darker for GL Premium, Savings, Competitiveness
  - Lower = darker for WC Rate (reverse scale)

### Performance
- SVG optimized for minimal file size
- ~5–10 KB of JS
- Runs only on the map page
- No external JS libraries or frameworks required

---

## 6. UX/UI Requirements

### Desktop Layout
1. Title
2. Four-button toggle bar
3. Map (SVG)
4. Info card below map

### Mobile Layout (<768px)
1. Title
2. Toggle bar
3. State dropdown
4. Info card below dropdown

### Styling
- **Buttons**: rounded, active button highlighted
- **Map**: neutral base with heatmap coloring
- **Tooltip**: dark background, white text, subtle shadow
- **Info card**: light background, rounded corners, subtle shadow

---

## 7. Acceptance Criteria
- ✅ All states + D.C. included with data
- ✅ Four toggles update map instantly
- ✅ Correct color scaling per metric (normal vs reverse)
- ✅ Desktop tooltips + info card work
- ✅ Mobile dropdown provides full functionality
- ✅ No external dependencies or licensing required
- ✅ Tested on major browsers and devices

---

## 8. Out of Scope (Phase 1)
- Animations beyond hover highlights
- Dynamic data loading from APIs or external sources
- Historical data comparison or time sliders
- Multi-country or regional maps

---

## 9. Timeline

**Week 1:**
- Finalize datasets
- Prepare clean SVG and embed in page

**Week 2:**
- Implement JS for coloring, toggles, tooltips, info card
- Style components for desktop and mobile

**Week 3:**
- QA on browsers and devices
- Stakeholder review and launch

---

## 10. Risks & Mitigations

**Risk: SVG file size too large**
- Mitigation: Optimize SVG paths, remove unused attributes

**Risk: Data changes require code edits**
- Mitigation: Keep dataset section clearly commented at top of script

**Risk: Small-screen usability suffers without map**
- Mitigation: Provide full dropdown experience with identical info

**Risk: Users may misinterpret metrics**
- Mitigation: Include plain-language subtext in info card/tooltips