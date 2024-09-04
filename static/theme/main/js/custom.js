(function ($) {

	"use strict";

	//brand part js
	$('.brand-main').slick({
		slidesToShow: 4,
		slidesToScroll: 1,
		autoplay: true,
		dots: false,
		arrows: false,
		autoplaySpeed: 2500,
		responsive: [
			{
				breakpoint: 576,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1,
				}
    },
			{
				breakpoint: 768,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1,
				}
    },
			{
				breakpoint: 992,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1,
				}
    },

  ]
	});

	//reviews part js
	$('.review-main').slick({
		slidesToShow: 2,
		slidesToScroll: 1,
		autoplay: true,
		dots: false,
		arrows: true,
		nextArrow: '#reviews .fa-arrow-right',
		prevArrow: '#reviews .fa-arrow-left',
		autoplaySpeed: 2500,
		responsive: [
			{
				breakpoint: 576,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
				}
    },
			{
				breakpoint: 768,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
				}
    },
			{
				breakpoint: 992,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1,
				}
    },

  ]
	});
	
    // preloader js
    $(window).on('load', function () {
        $('#preloader').delay(1000).fadeOut(1000);

    });
	
	//animation scroll js
	var html_body = $('html, body');
	$('.navbar a, #backtotop #backtotop-value').on('click', function () {
		if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
			var target = $(this.hash);
			target = target.length ? target : $('[name="' + this.hash.slice(1) + '"]');
			if (target.length) {
				html_body.animate({
					scrollTop: target.offset().top - 35
				}, 1500);
				return false;
			}
		}
	});

	// smooth scroll js 
	$(window).scroll(function () {
		var scrolling = $(this).scrollTop();
		var stikey = $('.sticky-top');
		var old_star = "images/star.png";
		var new_star = "images/star-red.png";

		if (scrolling >= 950 && scrolling <= 1910 ||
			scrolling >= 4150 && scrolling <= 5160) {
			$('#banner .marquee').addClass("marquee-white");
			$('.marquee img').attr('src', new_star);
		} else {
			$(stikey).removeClass("nav-bg");
			$('#banner .marquee').removeClass("marquee-white");
			$('.marquee img').attr('src', old_star);
		}

		if (scrolling >= 100) {
			$(stikey).addClass("nav-bg");
		} else {
			$(stikey).removeClass("nav-bg");
		}
	});

	// back to top
	$(document).ready(function () {
		let calcScrollValue = () => {
			let scrollProgress = document.getElementById("backtotop");
			let progressValue = document.getElementById("backtotop-value");
			let pos = document.documentElement.scrollTop;
			let calcHeight =
				document.documentElement.scrollHeight -
				document.documentElement.clientHeight;
			let scrollValue = Math.round((pos * 100) / calcHeight);
			if (pos > 100) {
				scrollProgress.style.display = "grid";
			} else {
				scrollProgress.style.display = "none";
			}
			scrollProgress.addEventListener("click", () => {
				document.documentElement.scrollTop = 0;
			});
			scrollProgress.style.background = `conic-gradient(#d71515 ${scrollValue}%, #FFF ${scrollValue}%)`;
		};

		window.onscroll = calcScrollValue;
		window.onload = calcScrollValue;
	});

	//parallax effect js
	var img_one = $('.banner-img.one');
	var banner_icon = $('.banner-icon');
	var img_two = $('.banner-img.two');

	var layer = $('.banner-images');

	layer.mousemove(function (e) {
		var ivalueX = (e.pageX * -1 / 30);
		var ivalueY = (e.pageY * -1 / 30);
		var cvalueX = (e.pageX * -1 / 40);
		var cvalueY = (e.pageY * -1 / 60);
		img_one.css('transform', 'translate3d(' + ivalueX + 'px,' + ivalueY + 'px, 0)rotate(6deg)');
		banner_icon.css('transform', 'translate3d(' + ivalueX + 'px,' + ivalueY + 'px, 0)rotate(20deg)');
		img_two.css('transform', 'translate3d(' + cvalueX + 'px,' + cvalueY + 'px, 0)');
	});

	// venobox player js
	new VenoBox({
		selector: ".button-circular, .veno-img",
		numeration: true,
		infinigall: true,
		share: true,
	});

	// counter part js
	$('.counter').counterUp();

}(jQuery));
