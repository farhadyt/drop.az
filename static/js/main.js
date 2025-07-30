// Səhifə tam yükləndikdən sonra bu kod işə düşsün
document.addEventListener('DOMContentLoaded', function() {
    
    // Header elementimizi seçirik
    const header = document.querySelector('.floating-header');

    // Əgər header yoxdursa, heç bir şey etmə
    if (!header) {
        return;
    }

    // Səhifənin scroll hərəkətlərinə qulaq asırıq
    window.addEventListener('scroll', function() {
        // Əgər yuxarıdan 50px-dən çox aşağı sürüşdürülübsə
        if (window.scrollY > 50) {
            // header-ə 'scrolled' class-ını əlavə et
            header.classList.add('scrolled');
        } else {
            // əks halda 'scrolled' class-ını sil
            header.classList.remove('scrolled');
        }
    });
});