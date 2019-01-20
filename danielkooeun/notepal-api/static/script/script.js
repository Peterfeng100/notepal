$(function() {
    let eTop = $('#section-2').offset().top;
    $(window).scroll(function () {
        if (screen.width > 500 ) {
            if (eTop - $(window).scrollTop() < 150) {
                $("header").addClass("changeColor")
                //$(".nav-a").css("color", "#501E3B");
                //$(".login").css("box-shadow", "0px 1px 4px rgba(0, 0, 0, .2)");
            }
            if (eTop - $(window).scrollTop() > 150) {
                $("header").removeClass("changeColor")
            }
        } else if (screen.width < 501) {
            $("header").addClass("changeColor")
        }
    });
 });

