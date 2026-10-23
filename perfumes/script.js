/* Scroll handler: updates --p custom property on each .stage based on scroll progress */
(function(){
  const stages = document.querySelectorAll('.stage');
  const onScroll = () => {
    stages.forEach(stage => {
      const rect = stage.getBoundingClientRect();
      const top = rect.top + window.scrollY; // stage top relative to document
      const height = stage.offsetHeight;
      const scrollY = window.scrollY;
      // progress: 0 when top of stage at viewport top, 1 when bottom passed
      let p = (scrollY - top) / height;
      p = Math.min(Math.max(p, 0), 1);
      stage.style.setProperty('--p', p);
    });
  };
  window.addEventListener('scroll', onScroll);
  // Initial call
  onScroll();
})();

/* IntersectionObserver to reveal elements with data-rev attribute */
const revObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if(entry.isIntersecting){
      entry.target.classList.add('in-view');
    }
  });
}, {threshold: 0.12});

document.querySelectorAll('[data-rev]').forEach(el => revObserver.observe(el));

/* Utility to split text into per-word spans for staggered animation */
function splitIntoSpans(selector){
  document.querySelectorAll(selector).forEach(el => {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = '';
    words.forEach((w,i)=>{
      const span = document.createElement('span');
      span.className = 'word';
      span.style.setProperty('--i', i);
      span.textContent = w + (i < words.length-1 ? ' ' : '');
      el.appendChild(span);
    });
  });
}
// Apply to headings and statements
splitIntoSpans('.hero-text .overline');
splitIntoSpans('.hero-text .wordmark');
splitIntoSpans('.statement .col');
splitIntoSpans('.headline');
splitIntoSpans('.caption');

/* CSS animation for per-word stagger via --i */
const style = document.createElement('style');
style.textContent = `
  [class*="word"] {
    opacity:0; transform:translateY(0.4em);
    animation: fadeUp 0.4s forwards;
    animation-delay: calc(var(--i) * 38ms);
  }
`;
document.head.appendChild(style);
