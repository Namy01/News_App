const toggleBtn = document.getElementById('toggle-btn');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('main-content');

toggleBtn.addEventListener('click', () => {
  sidebar.classList.toggle('hidden');
  if (sidebar.classList.contains('hidden')) {
    mainContent.classList.add('full-width');
  } else {
    mainContent.classList.remove('full-width');
  }
});