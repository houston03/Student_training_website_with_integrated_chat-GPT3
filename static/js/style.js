    const containers = document.querySelectorAll('.container');

    containers.forEach(container => {
      const fullscreenButton = container.querySelector('.full');
      const overlay = document.querySelector('.overlay');

      fullscreenButton.addEventListener('click', () => {
        container.classList.toggle('fullscreen');
        overlay.classList.toggle('show');

        // Изменяем иконку кнопки
        const icon = fullscreenButton.querySelector('i');
        icon.classList.toggle('bi-arrows-fullscreen');
        icon.classList.toggle('bi-arrows-angle-contract');

        // Увеличиваем размер текста и заголовка
        container.querySelectorAll('p, h4').forEach(element => {
          element.style.fontSize = container.classList.contains('fullscreen') ;
        });
      });
    });