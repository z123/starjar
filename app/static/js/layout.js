$(document).ready(function () {
    $('#login-button').on('click', function () {
        $('.ui.modal')
            .modal({
                transition: 'fade down'
            })
            .modal('show');
    });
});

