/* ==========================================================================
   abdallah consultancy firm — main.js  (jQuery 3.x)
   Features: theme toggle, mobile menu, sticky header + scroll progress,
   scroll reveal, animated counters, testimonial slider, FAQ accordion,
   expertise scroll-spy, articles (AJAX + filter + dialog), form validation,
   back-to-top.
   ========================================================================== */
(function ($) {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  $(function () {

    /* 1. Dark / light theme ------------------------------------------------ */
    function applyTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      $('.theme-toggle').attr({
        'aria-pressed': theme === 'dark',
        'aria-label': theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
      });
      $('meta[name="theme-color"]').attr('content', theme === 'dark' ? '#0D1615' : '#F6F8F7');
    }
    applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

    $('.theme-toggle').on('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem('theme', next); } catch (e) { /* storage unavailable */ }
    });

    /* 2. Mobile menu ------------------------------------------------------- */
    var $header = $('.site-header');
    var $navToggle = $('.nav-toggle');

    function setMenu(open) {
      $header.toggleClass('nav-open', open);
      $navToggle.attr('aria-expanded', open).find('.visually-hidden').text(open ? 'Close menu' : 'Open menu');
    }
    $navToggle.on('click', function () { setMenu(!$header.hasClass('nav-open')); });
    $('#nav a').on('click', function () { setMenu(false); });
    $(document).on('keydown', function (e) {
      if (e.key === 'Escape' && $header.hasClass('nav-open')) { setMenu(false); $navToggle.trigger('focus'); }
    });
    $(window).on('resize', function () { if (window.innerWidth >= 900) { setMenu(false); } });

    /* 3. Scroll: sticky header shadow, progress line, back-to-top --------- */
    var $progress = $('.progress');
    var $toTop = $('.to-top');
    var ticking = false;

    function onScroll() {
      var y = window.pageYOffset;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      $header.toggleClass('scrolled', y > 8);
      $progress.css('transform', 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')');
      $toTop.toggleClass('show', y > 600);
      ticking = false;
    }
    $(window).on('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
    });
    onScroll();

    $toTop.on('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      $('#main').trigger('focus');
    });

    /* 4. Scroll reveal ----------------------------------------------------- */
    var $reveal = $('.reveal');
    if (hasIO && !reduceMotion) {
      var revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            $(entry.target).addClass('in');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -5% 0px' });
      $reveal.each(function () { revealObserver.observe(this); });
    } else {
      $reveal.addClass('in');
    }

    /* 5. Animated counters ------------------------------------------------- */
    function runCounter(el) {
      var end = parseInt(el.getAttribute('data-count'), 10);
      var suffix = el.getAttribute('data-suffix') || '';
      if (reduceMotion) { el.textContent = end + suffix; return; }
      var duration = 1500;
      var start = null;
      function step(ts) {
        if (start === null) { start = ts; }
        var p = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(end * eased) + suffix;
        if (p < 1) { window.requestAnimationFrame(step); }
      }
      window.requestAnimationFrame(step);
    }
    var $counters = $('[data-count]');
    if (hasIO) {
      var counterObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { runCounter(entry.target); counterObserver.unobserve(entry.target); }
        });
      }, { threshold: 0.6 });
      $counters.each(function () { counterObserver.observe(this); });
    }

    /* 6. Testimonial slider ------------------------------------------------ */
    $('[data-slider]').each(function () {
      var $slider = $(this);
      var $track = $slider.find('.slides');
      var $slides = $track.children();
      var $dots = $slider.find('.dots');
      var $pause = $slider.find('.slider-pause');
      var total = $slides.length;
      var index = 0;
      var timer = null;
      var userPaused = reduceMotion;   // never autoplay for people who prefer less motion

      $slides.each(function (i) {
        $('<button type="button" class="dot"></button>')
          .attr('aria-label', 'Show review ' + (i + 1) + ' of ' + total)
          .on('click', function () { go(i); })
          .appendTo($dots);
      });

      function go(i) {
        index = (i + total) % total;
        $track.css('transform', 'translateX(' + (-100 * index) + '%)');
        $slides.each(function (n) { $(this).attr('aria-hidden', n === index ? 'false' : 'true'); });
        $dots.children().each(function (n) { $(this).attr('aria-current', n === index ? 'true' : 'false'); });
      }
      function play() {
        stop();
        if (!userPaused && total > 1) { timer = window.setInterval(function () { go(index + 1); }, 7000); }
      }
      function stop() { window.clearInterval(timer); timer = null; }
      function syncPauseButton() {
        $pause.attr('aria-pressed', userPaused).text(userPaused ? 'Play' : 'Pause');
      }

      $slider.find('.slider-prev').on('click', function () { go(index - 1); play(); });
      $slider.find('.slider-next').on('click', function () { go(index + 1); play(); });
      $pause.on('click', function () { userPaused = !userPaused; syncPauseButton(); play(); });
      $slider.on('mouseenter focusin', stop).on('mouseleave focusout', play);

      var touchX = null;
      $slider.on('touchstart', function (e) { touchX = e.originalEvent.touches[0].clientX; });
      $slider.on('touchend', function (e) {
        if (touchX === null) { return; }
        var dx = e.originalEvent.changedTouches[0].clientX - touchX;
        if (Math.abs(dx) > 50) { go(index + (dx < 0 ? 1 : -1)); }
        touchX = null;
      });

      go(0); syncPauseButton(); play();
    });

    /* 7. FAQ accordion ----------------------------------------------------- */
    $('.faq-q').on('click', function () {
      var $btn = $(this);
      var open = $btn.attr('aria-expanded') === 'true';
      $btn.attr('aria-expanded', !open).closest('.faq-item').toggleClass('open', !open);
    });

    /* 8. Expertise: highlight the section being read ----------------------- */
    var $areaLinks = $('.area-nav a');
    if ($areaLinks.length && hasIO) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var id = entry.target.id;
            $areaLinks.removeClass('active').removeAttr('aria-current');
            var $active = $areaLinks.filter('[href="#' + id + '"]').addClass('active').attr('aria-current', 'true');
            // keep the active chip visible in the horizontal mobile bar
            var list = $active.closest('ul')[0];
            if (list && list.scrollWidth > list.clientWidth) {
              list.scrollTo({ left: $active[0].offsetLeft - 16, behavior: reduceMotion ? 'auto' : 'smooth' });
            }
          }
        });
      }, { rootMargin: '-30% 0px -60% 0px' });
      $('.area').each(function () { spy.observe(this); });
    }

    /* 9. Articles: AJAX load, filter, search, dialog ----------------------- */
    var $cards = $('#article-cards');
    if ($cards.length) {
      var articles = [];
      var activeCategory = 'All';
      var query = '';
      var dialog = document.getElementById('article-dialog');

      var formatDate = function (iso) {
        var d = new Date(iso + 'T00:00:00');
        return isNaN(d) ? iso : d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
      };

      var buildChips = function () {
        var cats = ['All'];
        articles.forEach(function (a) { if (cats.indexOf(a.category) === -1) { cats.push(a.category); } });
        var $chips = $('#article-chips').empty();
        cats.forEach(function (c) {
          $('<button type="button" class="chip"></button>').text(c)
            .attr('aria-pressed', c === activeCategory)
            .on('click', function () {
              activeCategory = c;
              $chips.children().attr('aria-pressed', 'false');
              $(this).attr('aria-pressed', 'true');
              renderCards();
            }).appendTo($chips);
        });
      };

      var openArticle = function (a) {
        var $body = $('#dlg-content').empty();
        var $meta = $('<p class="card-meta"></p>').appendTo($body);
        $('<span></span>').text(a.category).appendTo($meta);
        $('<span></span>').text(formatDate(a.date)).appendTo($meta);
        $('<span></span>').text(a.readTime).appendTo($meta);
        if (a.placeholder) { $('<span class="tag">Placeholder article</span>').appendTo($meta); }
        $('<h2 id="dlg-title"></h2>').text(a.title).appendTo($body);
        (a.body || [a.excerpt]).forEach(function (para) { $('<p></p>').text(para).appendTo($body); });
        $('<p class="count"></p>').text('General information only. This is not legal advice.').appendTo($body);
        $('<a class="btn" href="contact.html#form">Schedule a legal consultation</a>').appendTo($body);
        if (dialog && dialog.showModal) { dialog.showModal(); } else if (dialog) { dialog.setAttribute('open', ''); }
      };

      var renderCards = function () {
        var q = query.trim().toLowerCase();
        var list = articles.filter(function (a) {
          var inCat = activeCategory === 'All' || a.category === activeCategory;
          var inText = !q || (a.title + ' ' + a.excerpt + ' ' + a.category).toLowerCase().indexOf(q) !== -1;
          return inCat && inText;
        });
        $cards.empty();
        $('#article-count').text(list.length === 1 ? 'Showing 1 article' : 'Showing ' + list.length + ' articles');

        if (!list.length) {
          $('<p class="empty"></p>').text('No articles match your search. Clear the search or choose "All".').appendTo($cards);
          return;
        }
        list.forEach(function (a, i) {
          var $card = $('<article class="card"></article>');
          $('<div class="thumb" aria-hidden="true"></div>').attr('data-tone', i % 3).appendTo($card);
          var $b = $('<div class="card-body"></div>').appendTo($card);
          var $meta = $('<p class="card-meta"></p>').appendTo($b);
          $('<span></span>').text(a.category).appendTo($meta);
          $('<span></span>').text(formatDate(a.date)).appendTo($meta);
          $('<span></span>').text(a.readTime).appendTo($meta);
          $('<h3></h3>').text(a.title).appendTo($b);
          $('<p></p>').text(a.excerpt).appendTo($b);
          if (a.placeholder) { $('<p><span class="tag">Placeholder article</span></p>').appendTo($b); }
          $('<button type="button" class="btn btn-ghost btn-sm"></button>')
            .text('Read article')
            .attr('aria-label', 'Read article: ' + a.title)
            .on('click', function () { openArticle(a); })
            .appendTo($b);
          $card.appendTo($cards);
        });
      };

      var start = function (data) {
        articles = data;
        buildChips();
        renderCards();
      };

      // Primary source: data/articles.json (AJAX). Works on any web server.
      // Fallback: the JSON copy inside articles.html, so the page also works
      // when opened straight from the file system (where AJAX is blocked).
      $.getJSON('data/articles.json').done(start).fail(function () {
        try { start(JSON.parse($('#articles-fallback').text())); }
        catch (e) { $('#article-count').text('Articles could not be loaded.'); }
      });

      $('#article-search').on('input', function () { query = this.value; renderCards(); });

      if (dialog) {
        $(dialog).on('click', function (e) { if (e.target === dialog) { dialog.close(); } });
        $('.dlg-close').on('click', function () { dialog.close(); });
      }
    }

    /* 10. Contact form (no backend) ---------------------------------------- */
    var $form = $('#contact-form');
    if ($form.length) {
      var messages = {
        name:    'Enter your full name (at least 2 characters).',
        email:   'Enter a valid email address, for example name@example.com.',
        phone:   'Enter a phone number with at least 7 digits, for example +230 5xxx xxxx.',
        area:    'Choose the practice area that fits your matter.',
        message: 'Describe your matter in at least 20 characters so we can help.',
        consent: 'Tick the box to confirm you agree before sending.'
      };
      var validators = {
        name:    function (v) { return v.trim().length >= 2; },
        email:   function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); },
        phone:   function (v) { return /^\+?[0-9\s\-()]{7,20}$/.test(v.trim()) && v.replace(/\D/g, '').length >= 7; },
        area:    function (v) { return v !== ''; },
        message: function (v) { return v.trim().length >= 20; },
        consent: function (v, $el) { return $el.is(':checked'); }
      };

      var validateField = function (name) {
        var $el = $form.find('[name="' + name + '"]');
        var ok = validators[name]($el.val() || '', $el);
        var $wrap = $el.closest('.field');
        $wrap.toggleClass('invalid', !ok);
        $el.attr('aria-invalid', !ok);
        $('#' + name + '-error').text(ok ? '' : messages[name]);
        return ok;
      };

      $.each(validators, function (name) {
        var $el = $form.find('[name="' + name + '"]');
        $el.on('blur change', function () { validateField(name); });
        $el.on('input', function () { if ($el.closest('.field').hasClass('invalid')) { validateField(name); } });
      });

      $('#message').on('input', function () { $('#message-count').text(this.value.length + ' / 1000'); });

      // Pre-select the practice area from links such as contact.html?area=family
      var areaParam = new URLSearchParams(window.location.search).get('area');
      if (areaParam && $('#area option[value="' + areaParam + '"]').length) { $('#area').val(areaParam); }

      $form.on('submit', function (e) {
        e.preventDefault();
        var firstInvalid = null;
        $.each(validators, function (name) {
          if (!validateField(name) && !firstInvalid) { firstInvalid = name; }
        });
        if (firstInvalid) { $form.find('[name="' + firstInvalid + '"]').trigger('focus'); return; }

        var $btn = $form.find('button[type="submit"]').prop('disabled', true).text('Sending…');
        var payload = $form.serialize();

        // DEMO ONLY: there is no backend, so the request is simulated.
        // To send real messages, replace the timeout with an AJAX call, e.g.:
        //   $.ajax({ url: 'https://formspree.io/f/YOUR_ID', method: 'POST', data: payload,
        //            headers: { Accept: 'application/json' } }).done(showSuccess).fail(showFailure);
        window.setTimeout(function () { showSuccess(payload); }, 900);

        function showSuccess() {
          $('#success-name').text($('#name').val().trim().split(' ')[0]);
          $('#success-email').text($('#email').val().trim());
          $form.attr('hidden', true);
          $('#form-success').removeAttr('hidden').trigger('focus');
          $form[0].reset();
          $('#message-count').text('0 / 1000');
          $btn.prop('disabled', false).text('Send message');
        }
      });

      $('#send-another').on('click', function () {
        $('#form-success').attr('hidden', true);
        $form.removeAttr('hidden');
        $('#name').trigger('focus');
      });
    }

  });
})(jQuery);
