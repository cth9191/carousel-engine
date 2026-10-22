// A filled slides[] for a copy of templates/03-command-press/slides.html (placeholder topic "linked notes"; it made
// samples/smoke-bake-*.png): a model sheet with a FIG plate, a peak sheet with prompt-NN.html, and the CTA with an ink
// stub card. Paste over the template's slides[] and delete its samples.
  const slides = [
    { name:'Cover', cover:true, coverImg:'cover.png' },
    {
      name:'Model — How a link works',
      chip:'PART 02', rev:'REV A',
      headlineHTML:'/LINK', fig:'FIG.2 — 1 note · 2 link · 3 note',
      body:'A link is a pointer from <strong>one note</strong> to <strong>another</strong>.<br><br>Open either note and the other one is <span class="accent">one click away.</span>',
      hero:{ type:'image', src:'assets/fig-model.png', maxH:470, focus:'center' },
      defaults:{ headSize:240, bodySize:33, bodyTop:466, heroBottom:150 },
    },
    {
      name:'Peak — The prompt',
      chip:'PROMPT 07', rev:'REV A',
      headlineHTML:'/PASTE', fig:'FIG.7 — copy it as written',
      body:'One prompt does the first pass for you.<br><br>Read the links it proposes, then <span class="accent">keep the ones that fit.</span>',
      hero:{ type:'image', src:'assets/prompt-07.png' },
      defaults:{ headSize:240, bodySize:33, bodyTop:466, heroBottom:150 },
    },
    {
      name:'CTA',
      chip:'OUTRO', rev:'REV A',
      headlineHTML:'LINKS', fig:'FIG.8 — the full setup, in your DMs',
      body:'Comment <strong>LINKS</strong> and I’ll send you <span class="accent">the full notes setup.</span>',
      hero:{ type:'image', src:'assets/stub-08.png' },
      defaults:{ headSize:240, bodySize:40, bodyTop:500, heroBottom:150 },
    },
  ];
