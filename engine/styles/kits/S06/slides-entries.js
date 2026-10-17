// Example slides[] for an S06 deck (a templates/01-graph-paper-cream/slides.html copy): the entries behind
// samples/slide-02.png and samples/slide-03.png, on a placeholder topic ("top 3 browser-testing repos").
// The CTA uses the template's keyword mode (ctaKeyword + ctaDeliverable); TOTAL_SLIDES and the NN / TT
// counter come from slides.length in the template itself.
  const slides = [
    { name: 'Cover', cover: true, coverImg: 'final/slide-01.png', slideIndex: 0 },
    {
      name: 'Playwright',
      headlineHTML: '#1: <span class="accent">Playwright</span><br>tests every browser<br>at once',
      layered: true,
      heroBg: 'assets/hero-playwright.png', // README capture cropped to the content column (no contributor avatars)
      repoCard: {
        owner: 'microsoft', name: 'playwright', title: 'playwright',
        desc: 'A framework for web testing and automation.',
        lang: 'TypeScript', langColor: '#3178c6', stars: '97.9k', // read off the repo page on posting day
      },
      body: 'One API drives Chromium, Firefox and WebKit, so one test file covers all three',
      slideIndex: 1,
      defaults: { cardX: 24, cardY: 40, cardW: 44, tilt: 0 },
    },
    {
      name: 'CTA',
      cta: true,
      ctaHeadline: 'WANT<br>ALL 3?',
      ctaKeyword: 'TESTS',
      ctaDeliverable: 'I’ll send you the full list with install links.',
      ctaHandle: '{{BRAND}}', // your handle; the deck copy replaces {{BRAND}} from engine/brand.json
      slideIndex: 2,
    },
  ];
