const filters = document.querySelector('.filters');
const buttons = filters.querySelectorAll('button');
const entries = document.querySelectorAll('[data-category]');
const cards = document.querySelectorAll('.card');
const count = document.querySelector('#count');

filters.hidden = false;
for (const button of buttons) {
  button.addEventListener('click', () => {
    const category = button.dataset.filter;
    for (const item of entries) {
      item.hidden = Boolean(category) && item.dataset.category !== category;
    }
    for (const control of buttons) {
      control.setAttribute('aria-pressed', String(control === button));
    }
    const visible = Array.from(cards).filter(card => !card.hidden).length;
    count.textContent = `${visible} 家店`;
  });
}
