# Master specification (verbatim source of truth)

> Stored so any later session can continue against the original requirements.

```text
Final master prompt for Claude Code
You are the principal architect, interaction-design researcher, open-source maintainer, frontend engineer,
accessibility specialist, application-security reviewer and Agent Skills engineer responsible for creating
a production-grade open-source project.
 
PROJECT NAME
Open Interaction Intelligence
 
REPOSITORY SLUG
open-interaction-intelligence
 
MISSION
Build an open-source Agent Skill and supporting local knowledge system that helps Claude Code and compatible
AI coding agents research, discover, select, adapt, implement and validate user-interface interactions,
animations, motion patterns and visual effects for websites and web applications.
 
The system must support:
- enterprise applications;
- ERP and CRM systems;
- dashboards and analytics;
- project-management and collaboration products;
- SaaS products;
- AI and developer tools;
- corporate and SaaS marketing websites;
- e-commerce websites;
- product-launch websites;
- documentation websites;
- editorial and portfolio experiences;
- experimental web experiences.
 
This must not become:
- a list of effect websites;
- a collection of copied components;
- a prompt that adds random animation;
- a tool that executes arbitrary internet code;
- a package that ignores licensing, accessibility or performance.
 
Its central principle is:
 
First determine what the user needs to understand, feel or accomplish.
Then select the least complex interaction that achieves that objective.
 
======================================================================
OPERATING MODE
======================================================================
 
Work autonomously and continue beyond planning.
 
Do not stop after creating an architecture outline.
Do not create placeholder-only files and claim completion.
Do not ask me to make routine engineering decisions.
Make reasoned decisions, document them and proceed.
 
Ask only when progress is impossible without information that cannot be safely inferred, such as:
- an unavailable GitHub organisation name;
- missing GitHub authentication;
- an irreversible operation requiring explicit approval.
 
Work in defined phases. At the end of each phase:
1. inspect all created or changed files;
2. run relevant validation;
3. correct identified issues;
4. update project status;
5. commit the completed phase with a meaningful conventional commit.
 
Never push broken or partially validated work.
 
======================================================================
PHASE 0 - ENVIRONMENT, REPOSITORY AND SAFETY
======================================================================
 
Before creating files:
 
1. Inspect the current directory.
2. Determine whether it is already inside a Git repository.
3. Do not modify an unrelated project.
4. If needed, create:
   open-interaction-intelligence/
5. Enter the new directory.
6. Check:
   - Git;
   - Python;
   - Node.js and package manager if available;
   - Docker or compatible sandbox runtime if available;
   - GitHub CLI;
   - `gh auth status`;
   - active Git username and email.
7. Never print or store access tokens, secrets, SSH keys or private configuration.
8. Create a suitable `.gitignore`.
9. Initialise Git when required.
10. Use `main` as the default branch.
11. Never force-push.
12. Never overwrite an existing unrelated remote repository.
13. Create an architecture decision record before implementation.
14. Create a persistent phase-status file so a later Claude Code session can continue reliably.
 
Use conventional commits and commit only validated work.
 
======================================================================
PHASE 1 - PRODUCT AND INTERACTION INTELLIGENCE MODEL
======================================================================
 
The skill must reason progressively before considering an effect.
 
LEVEL 1 - DEVELOPMENT PURPOSE
- new website;
- new web application;
- existing product improvement;
- component development;
- design-system development;
- interaction audit;
- accessibility or performance remediation.
 
LEVEL 2 - PRODUCT TYPE
 
Web applications:
- enterprise application;
- ERP;
- CRM;
- project-management system;
- financial application;
- analytics dashboard;
- collaboration product;
- consumer SaaS;
- AI application;
- developer tool;
- marketplace;
- creative tool.
 
Websites:
- corporate website;
- SaaS marketing website;
- product-launch website;
- e-commerce website;
- documentation website;
- editorial website;
- event website;
- agency website;
- portfolio;
- immersive experience.
 
LEVEL 3 - USER INTENT
- complete a task;
- enter information;
- review information;
- compare options;
- monitor status;
- navigate;
- discover content;
- evaluate a product;
- purchase;
- learn;
- collaborate;
- configure a system.
 
LEVEL 4 - PAGE OR SCREEN TYPE
 
Web-application screens:
- login;
- onboarding;
- dashboard;
- list;
- table;
- form;
- record details;
- kanban;
- timeline;
- calendar;
- command palette;
- settings;
- notifications;
- empty state;
- loading state;
- error state;
- confirmation state.
 
Website sections:
- hero;
- product demonstration;
- features;
- social proof;
- testimonials;
- pricing;
- comparison;
- case study;
- FAQ;
- call to action;
- navigation;
- footer.
 
LEVEL 5 - INTERACTION OBJECTIVE
- attract attention;
- explain hierarchy;
- show system feedback;
- preserve spatial continuity;
- demonstrate cause and effect;
- guide attention;
- reduce perceived waiting;
- confirm completion;
- prevent errors;
- strengthen affordance;
- improve discoverability;
- create emotional impact.
 
LEVEL 6 - PATTERN
Select a user-experience pattern that solves the identified problem.
 
LEVEL 7 - EFFECT
Select a low-level visual or motion technique only after the pattern is known.
 
LEVEL 8 - IMPLEMENTATION
Choose the simplest framework-native, accessible and maintainable implementation.
 
The system must search for a pattern before searching for an effect.
 
======================================================================
PHASE 2 - RESEARCH 50 TO 100 PUBLIC SOURCES
======================================================================
 
Design and execute a repeatable research methodology for approximately 50-100 legitimate public sources.
 
Prioritise official websites, official documentation and official repositories.
 
Research categories must include:
 
A. ANIMATED COMPONENT COLLECTIONS
- React Bits;
- Vue Bits;
- Svelte Bits;
- Magic UI;
- Aceternity UI;
- Motion Primitives;
- Animate UI;
- Animata;
- Fancy Components;
- Cult UI;
- Kokonut UI;
- Uiverse;
- Hover.dev;
- SmoothUI;
- GodUI;
- other maintained public animated-component collections discovered during research.
 
B. ACCESSIBLE UI FOUNDATIONS
- shadcn/ui;
- Radix UI;
- Base UI;
- React Aria;
- Headless UI;
- Ark UI;
- Reka UI;
- shadcn-vue;
- Bits UI;
- Melt UI.
 
C. ANIMATION ENGINES
- Motion;
- GSAP;
- Anime.js;
- AutoAnimate;
- React Spring;
- VueUse Motion;
- Motion for Vue;
- native Svelte motion;
- Theatre.js;
- other relevant maintained libraries.
 
D. BROWSER-NATIVE TECHNOLOGIES
- CSS transitions;
- CSS keyframes;
- CSS scroll-driven animations;
- Web Animations API;
- View Transitions API;
- Intersection Observer;
- Resize Observer;
- Pointer Events;
- SVG animation;
- Canvas API;
- WebGL;
- WebGPU where justified.
 
E. SCROLLING AND TRANSITIONS
- ScrollTrigger;
- Lenis;
- Locomotive Scroll;
- ScrollReveal;
- AOS;
- Barba.js;
- Swup;
- browser View Transitions examples.
 
F. CANVAS, PARTICLES AND GENERATIVE SYSTEMS
- tsParticles;
- PixiJS;
- p5.js;
- OGL;
- regl;
- Paper.js;
- Fabric.js;
- Konva;
- Vanta.js.
 
G. 3D AND SHADER ECOSYSTEMS
- Three.js;
- React Three Fiber;
- TresJS;
- Threlte;
- Babylon.js;
- Curtains.js;
- The Book of Shaders;
- ShaderToy as reference-only where appropriate;
- Spline as a tooling reference.
 
H. SVG, ILLUSTRATION AND ICON MOTION
- Lottie;
- Rive;
- Vivus;
- Rough Notation;
- public animated-icon libraries;
- public SVG-animation references.
 
I. CREATIVE-DEVELOPMENT REFERENCES
- Codrops;
- Awwwards developer resources;
- Hoverstat.es;
- Godly;
- SiteInspire;
- reputable curated website galleries.
 
Treat visual galleries as inspiration, not automatically reusable code.
 
J. ENTERPRISE MOTION AND INTERACTION GUIDANCE
- Material Design;
- Apple Human Interface Guidelines;
- Microsoft Fluent;
- IBM Carbon;
- Shopify Polaris;
- Atlassian Design System;
- GitHub Primer;
- Adobe Spectrum;
- Salesforce Lightning;
- Ant Design.
 
For each source, record:
- canonical name;
- official homepage;
- official repository;
- source category;
- supported frameworks;
- implementation technologies;
- dependency model;
- delivery model;
- maintenance status;
- documentation quality;
- accessibility maturity;
- performance characteristics;
- licence identifier;
- licence reference;
- redistribution status;
- attribution requirements;
- free/open-source/source-available/freemium/paid classification;
- suitable contexts;
- unsuitable contexts;
- strengths;
- weaknesses;
- last-reviewed date;
- evidence references;
- confidence level;
- trust tier.
 
Do not fabricate facts.
If internet access is unavailable, create the full research pipeline and mark records as
`pending-verification`. Never present assumptions as verified research.
 
======================================================================
PHASE 3 - COMPONENT-LEVEL CATALOGUE
======================================================================
 
A source is not complete merely because its homepage was reviewed.
 
For every selected source, discover its publicly accessible component or effect catalogue where technically
and legally possible.
 
Create one machine-readable record per component or distinct effect.
 
Record:
- component ID;
- component name;
- source;
- canonical component page;
- official repository path or registry entry;
- preview availability;
- supported framework;
- styling technology;
- animation technology;
- dependencies;
- required assets;
- browser requirements;
- installation method;
- copy-paste availability;
- licence;
- component-level exceptions;
- attribution;
- redistribution permission;
- commercial-use status;
- modification status;
- accessibility status;
- reduced-motion support;
- responsive behaviour;
- performance cost;
- complexity;
- quality status;
- verification date;
- evidence.
 
Assign each component one usability mode:
 
1. `bundled`
   Compatible code may legally be included in this repository.
 
2. `installable`
   The skill may install the component through the official package or registry.
 
3. `adaptable`
   The original code is not redistributed; the interaction concept may be independently implemented.
 
4. `reference-only`
   Metadata and design understanding only. Do not copy or create a substantially identical implementation.
 
5. `rejected`
   Unsafe, unlicensed, copied, malicious, broken, inaccessible or insufficient quality.
 
No component may be labelled usable until licensing and technical requirements are verified.
 
Build a source-by-source completeness report:
- total public components discovered;
- verified;
- bundled;
- installable;
- adaptable;
- reference-only;
- rejected;
- pending review.
 
Do not claim complete coverage without component-level records and evidence.
 
======================================================================
PHASE 4 - EFFECT, PATTERN AND RECIPE TAXONOMIES
======================================================================
 
Enforce these definitions:
 
EFFECT
A low-level visual or motion technique, such as:
- blur reveal;
- spring scale;
- crossfade;
- pointer spotlight;
- gradient movement;
- perspective tilt.
 
PATTERN
A user-experience solution to a problem, such as:
- optimistic save feedback;
- shared-element navigation;
- progressive onboarding;
- drag-and-drop feedback;
- skeleton loading.
 
RECIPE
A tested framework-specific implementation of a pattern using one or more effects.
 
Build machine-readable taxonomies covering:
 
Effects:
- text reveal and kinetic typography;
- blur, shimmer, gradient and counter effects;
- backgrounds, auroras, beams, grids, noise and particles;
- cards, tilt, magnetism, spotlights, borders and glass surfaces;
- navigation and command-palette motion;
- route, shared-element and layout transitions;
- scroll reveal, parallax, pinned storytelling and progress;
- pointer and cursor effects;
- loading, skeleton and progress states;
- save, success, validation and error feedback;
- drag-and-drop and reordering;
- table, kanban, timeline and chart motion;
- SVG;
- canvas;
- 3D;
- WebGL and shaders.
 
Patterns must include at least:
- optimistic save;
- pending/saving/saved state;
- inline validation;
- destructive confirmation;
- expandable details;
- drill-down continuity;
- shared-element navigation;
- command-palette reveal;
- contextual action disclosure;
- progressive onboarding;
- skeleton loading;
- streaming indication;
- empty-state guidance;
- drag feedback;
- kanban movement;
- filter/sort transition;
- row insertion/removal;
- status change;
- notification entrance;
- undo;
- upload progress;
- processing state;
- success confirmation;
- error recovery;
- scroll storytelling;
- product demonstration;
- comparison highlighting.
 
Anti-patterns must include:
- decoration-only animation;
- excessive entrance animation;
- scroll hijacking;
- forced custom cursor;
- hidden essential controls;
- long success animation;
- confetti for frequent actions;
- layout-jank animation;
- infinite motion in work areas;
- stacked glow effects;
- excessive glassmorphism;
- unnecessary 3D;
- fake loading;
- motion-only status;
- no reduced-motion support;
- gratuitous dependency installation.
 
======================================================================
PHASE 5 - SECURE SOURCE CONNECTORS AND INGESTION
======================================================================
 
Build a secure connector-based retrieval system.
 
The system must never directly scrape, execute and install arbitrary website code into a user project.
 
Required pipeline:
 
discover
→ verify official source
→ retrieve into quarantine
→ pin version and checksum
→ identify licence
→ static security analysis
→ dependency inspection
→ behaviour classification
→ accessibility and performance review
→ approve, adapt, reference or reject
→ controlled installation
 
Create source-specific connectors where justified and a strict generic official-GitHub connector.
 
Suggested structure:
 
connectors/
├── source-specific/
│   ├── react-bits/
│   ├── magic-ui/
│   ├── aceternity-ui/
│   ├── motion-primitives/
│   ├── uiverse/
│   └── ...
└── generic-github/
 
Each connector may:
- read public metadata;
- discover public component pages;
- retrieve code only from approved official locations;
- identify official package/registry installation;
- collect licence and attribution;
- store retrieved material in quarantine.
 
A connector must not:
- execute downloaded code;
- run install scripts;
- modify a target project;
- follow unknown domains;
- access local secrets;
- download or open arbitrary binaries.
 
Create three operating modes:
 
1. CATALOGUE-ONLY MODE
   Metadata and references only; no source retrieval.
 
2. REVIEW MODE
   Retrieve untrusted text into a disposable quarantine area for static review.
   Do not execute it.
 
3. APPROVED INSTALLATION MODE
   Only approved registry entries may be applied to a target project through a controlled patch.
 
The default runtime mode must be:
OFFLINE APPROVED REGISTRY
 
Internet retrieval must occur only through an explicit source-refresh or new-source workflow.
 
======================================================================
PHASE 6 - SECURITY CONTROLS
======================================================================
 
Implement the following controls.
 
DOMAIN POLICY
- explicit allowlist;
- block unknown redirects;
- block URL shorteners;
- block IP-address URLs unless explicitly approved;
- block localhost;
- block private network ranges;
- block unapproved asset hosts.
 
OFFICIAL SOURCE VERIFICATION
Prefer:
1. official tagged repository release;
2. official package registry;
3. official component registry;
4. pinned official commit;
5. webpage source only as a last resort.
 
PINNING AND INTEGRITY
Store:
- version;
- tag;
- commit hash;
- retrieval date;
- SHA-256 checksum.
 
QUARANTINE
Use an isolated structure such as:
.oii/
├── quarantine/
├── reviewed/
├── approved/
└── rejected/
 
NO EXECUTION DURING INGESTION
Do not:
- run `npm install`;
- run lifecycle scripts;
- execute JavaScript;
- run shell commands from documentation;
- open downloaded binaries;
- expose environment variables;
- expose home-directory files;
- expose SSH or GitHub credentials.
 
STATIC SECURITY SCANNING
Detect or flag:
- `eval`;
- `new Function`;
- dynamic code execution;
- child-process execution;
- shell execution;
- remote code loading;
- undocumented `fetch`, XHR or WebSocket use;
- cookie access;
- local/session storage;
- clipboard access;
- service workers;
- camera, microphone or geolocation;
- iframe injection;
- unsafe HTML insertion;
- analytics or telemetry;
- obfuscation;
- embedded secrets;
- crypto-mining patterns;
- remote script injection.
 
Not every occurrence is malicious, but every flagged occurrence must be reviewed.
 
DEPENDENCY INSPECTION
Inspect:
- direct dependencies;
- transitive dependencies;
- peer dependencies;
- optional dependencies;
- lifecycle scripts;
- maintainer and package identity;
- typosquatting risk;
- deprecation;
- unresolved advisories;
- unexpected dependency growth;
- licence compatibility.
 
BROWSER-BEHAVIOUR POLICY
An ordinary effect component should not require:
- cookies;
- persistent storage;
- clipboard;
- geolocation;
- camera;
- microphone;
- service worker;
- analytics;
- persistent WebSockets;
- remote executable scripts.
 
Any such behaviour requires explicit justification and approval.
 
NETWORK POLICY
Prefer self-contained components.
Reject or quarantine effects that:
- dynamically fetch executable content;
- load remote JavaScript;
- send telemetry;
- call undocumented APIs;
- embed tracking;
- depend on untrusted hosts.
 
LICENCE GATE
Unknown licence means `reference-only`, never bundled.
 
CLEAN-ROOM ADAPTATION
For restricted sources:
- retain no source code;
- record the interaction objective and behaviour;
- write a framework-neutral algorithm;
- implement independently;
- document inspiration and provenance;
- avoid line-by-line, structure-by-structure or distinctive-copy recreation.
 
SANDBOXED EXECUTION
When execution is necessary, use a disposable sandbox with:
- no secrets;
- no host network by default;
- no SSH keys;
- no GitHub credentials;
- no home-directory mount;
- CPU and memory limits;
- timeout;
- ephemeral filesystem;
- read-only base where practical.
 
INSTALLATION DIFF AND ROLLBACK
Before modifying a real project:
- inspect the target;
- generate a file/dependency plan;
- show source and licence;
- show security findings;
- show scripts;
- show dependency impact;
- create a rollback snapshot;
- apply a controlled patch;
- run validation;
- automatically revert if validation fails.
 
Do not run third-party installers directly against the target project.
 
NO AUTOMATIC NEW DEPENDENCY
Prefer:
1. dependency-free implementation;
2. existing project dependency;
3. original internal recipe;
4. approved lightweight dependency;
5. heavier dependency only with clear justification.
 
PROVENANCE MANIFEST
Generate a machine-readable manifest for every installed component:
- component;
- implementation ID;
- source type;
- inspiration sources;
- source version/commit;
- licence;
- installation date;
- created/modified files;
- dependencies;
- security review;
- accessibility support;
- reduced-motion behaviour.
 
TRUST TIERS
- Tier 1: official browser/framework documentation;
- Tier 2: established open-source project;
- Tier 3: maintained component library with clear ownership;
- Tier 4: community contribution;
- Tier 5: unknown or unverifiable.
 
Lower trust requires stronger review.
Tier 5 is reference-only or rejected.
 
Create malicious fixtures proving the controls catch:
- `eval`;
- package `postinstall`;
- remote script loader;
- cookie access;
- unknown licence;
- redirect to a private IP;
- obfuscated JavaScript;
- telemetry;
- suspicious binary asset.
 
Document that the system reduces risk but cannot guarantee that third-party code is completely safe.
 
======================================================================
PHASE 7 - LICENSING AND SOURCE GOVERNANCE
======================================================================
 
Public visibility is not permission to redistribute.
 
Classify sources:
- redistributable;
- adaptable-concept;
- reference-only;
- rejected.
 
Hard rules:
- never copy premium components;
- never reconstruct paid components from previews;
- never remove attribution;
- never copy code with unclear licensing;
- never treat source-available or Commons-Clause terms as ordinary permissive open source;
- never allow the project licence to override third-party obligations;
- record provenance for every recipe;
- label original implementations `original`;
- preserve third-party notices.
 
Create:
- `LICENSE`;
- `LICENSE_POLICY.md`;
- `THIRD_PARTY_SOURCES.md`;
- machine-readable licence records;
- contribution rules for provenance;
- clean-room adaptation procedure;
- automated validation for missing or incompatible licence metadata.
 
Choose MIT or Apache-2.0 for original project code after documenting the decision.
 
======================================================================
PHASE 8 - CANONICAL SELECTION AND DEDUPLICATION
======================================================================
 
Equivalent effects will appear in multiple libraries.
 
Do not bundle five nearly identical spotlight cards.
 
For each effect family:
1. identify duplicates;
2. compare alternatives;
3. select canonical approaches;
4. retain comparison metadata;
5. explain the selection.
 
Select canonical implementations using:
- licence compatibility;
- accessibility;
- source quality;
- performance;
- maintenance;
- dependency weight;
- framework portability;
- responsiveness;
- reduced-motion support;
- visual quality;
- customisability.
 
For each family, identify where possible:
- preferred no-dependency implementation;
- preferred lightweight implementation;
- preferred high-fidelity implementation;
- preferred enterprise implementation;
- preferred marketing implementation;
- preferred React implementation;
- preferred Vue implementation;
- preferred Svelte implementation;
- preferred vanilla implementation.
 
======================================================================
PHASE 9 - FRAMEWORK ADAPTATION
======================================================================
 
Use this model:
 
interaction concept
→ framework-neutral algorithm
→ framework adapter
→ project-specific implementation
 
Support:
- browser-native;
- React;
- Vue;
- Svelte;
- Angular;
- vanilla JavaScript;
- Tailwind;
- Frappe + Vue.
 
Vue and Frappe-Vue are first-class targets.
 
Preferred implementation order:
1. browser-native CSS;
2. native framework transitions;
3. existing project dependency;
4. Web Animations API;
5. View Transitions API;
6. lightweight approved motion dependency;
7. GSAP when justified;
8. Canvas;
9. Three.js/WebGL only when necessary.
 
Never install React into Vue, Svelte or Angular to obtain an effect.
 
Every adapter must document:
- idiomatic structure;
- lifecycle handling;
- cleanup;
- SSR;
- hydration;
- keyboard behaviour;
- pointer and coarse-pointer support;
- responsive behaviour;
- reduced motion;
- testing;
- dependency trade-offs.
 
Create a meaningful normalised component contract where applicable:
- class/style overrides;
- design-token compatibility;
- intensity;
- duration;
- delay;
- easing;
- disable-animation;
- reduced-motion strategy;
- responsive controls;
- accessible labels;
- event callbacks.
 
Do not force an artificial generic API where it harms quality.
 
======================================================================
PHASE 10 - QUALITY PROFILES
======================================================================
 
Create:
- enterprise-strict;
- saas-balanced;
- marketing-expressive;
- ecommerce-conversion;
- documentation-calm;
- editorial-storytelling;
- portfolio-creative;
- experimental;
- low-power-device;
- accessibility-first.
 
Each profile defines:
- goals;
- preferred patterns;
- restricted effects;
- continuous-motion policy;
- dependency budget;
- performance budget;
- maximum high-attention effects per viewport;
- reduced-motion policy;
- mobile constraints.
 
Support page-level overrides, for example:
- enterprise application overall;
- SaaS-balanced login;
- SaaS-balanced onboarding;
- marketing-expressive public product page.
 
======================================================================
PHASE 11 - ACCESSIBILITY
======================================================================
 
Accessibility is mandatory, not optional.
 
Require:
- `prefers-reduced-motion`;
- static or instant fallback;
- no motion-only meaning;
- keyboard operation;
- focus preservation;
- visible focus;
- appropriate live-region feedback;
- no seizure-risk flashing;
- no essential hover-only controls;
- pointer alternatives;
- coarse-pointer behaviour;
- readable contrast;
- zoom support;
- responsive support;
- no obstructive forced autoplay.
 
Clearly separate automated checks from human-review requirements.
 
Create a dedicated accessibility review skill and evaluation suite.
 
======================================================================
PHASE 12 - PERFORMANCE
======================================================================
 
Create budgets for:
- enterprise applications;
- marketing pages;
- mobile;
- low-power devices.
 
Review:
- bundle increase;
- direct and transitive dependencies;
- frame stability;
- layout shifts;
- long tasks;
- main-thread work;
- GPU usage;
- memory growth;
- offscreen animation;
- event-listener cleanup;
- canvas/WebGL lifecycle;
- battery impact;
- reduced-data behaviour where applicable.
 
Prefer `transform` and `opacity`.
Pause or disable offscreen continuous motion.
Do not claim measured performance without measurement.
 
======================================================================
PHASE 13 - REPOSITORY ARCHITECTURE
======================================================================
 
Build a maintainable repository. Refine this structure if necessary, but preserve separation of concerns:
 
open-interaction-intelligence/
├── SKILL.md
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── CHANGELOG.md
├── LICENSE
├── LICENSE_POLICY.md
├── THIRD_PARTY_SOURCES.md
├── pyproject.toml
├── package.json
├── Makefile
├── .gitignore
├── .editorconfig
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── dependabot.yml
├── skills/
│   ├── web-experience-orchestrator/
│   ├── product-context-analysis/
│   ├── interaction-design/
│   ├── effect-discovery/
│   ├── effect-selection/
│   ├── framework-adaptation/
│   ├── motion-accessibility/
│   ├── motion-performance/
│   ├── implementation-validation/
│   └── source-governance/
├── agents/
│   ├── experience-architect.md
│   ├── source-researcher.md
│   ├── interaction-designer.md
│   ├── implementation-engineer.md
│   ├── security-reviewer.md
│   ├── accessibility-reviewer.md
│   ├── performance-reviewer.md
│   └── visual-quality-reviewer.md
├── intelligence/
│   ├── product-types/
│   ├── page-types/
│   ├── user-intents/
│   ├── interaction-problems/
│   ├── effect-taxonomy/
│   ├── selection-policies/
│   ├── anti-patterns/
│   └── quality-profiles/
├── registry/
│   ├── sources/
│   ├── components/
│   ├── effects/
│   ├── patterns/
│   ├── recipes/
│   ├── dependencies/
│   └── licenses/
├── connectors/
│   ├── source-specific/
│   └── generic-github/
├── ingestion/
│   ├── discovery/
│   ├── retrieval/
│   ├── quarantine/
│   └── normalisation/
├── security/
│   ├── domain-policy.yml
│   ├── network-policy.yml
│   ├── dangerous-patterns.yml
│   ├── dependency-policy.yml
│   ├── sandbox-policy.yml
│   └── trust-policy.yml
├── scanners/
│   ├── source_scanner.py
│   ├── dependency_scanner.py
│   ├── license_scanner.py
│   ├── behaviour_scanner.py
│   └── secret_scanner.py
├── adapters/
│   ├── browser-native/
│   ├── react/
│   ├── vue/
│   ├── svelte/
│   ├── angular/
│   ├── vanilla/
│   ├── tailwind/
│   └── frappe-vue/
├── implementations/
│   ├── browser-native/
│   ├── react/
│   ├── vue/
│   ├── svelte/
│   ├── vanilla/
│   └── frappe-vue/
├── workflows/
│   ├── build-new-website.md
│   ├── build-new-web-app.md
│   ├── improve-existing-ui.md
│   ├── audit-motion.md
│   ├── select-effects.md
│   ├── refresh-sources.md
│   ├── review-component.md
│   ├── implement-pattern.md
│   ├── convert-framework.md
│   ├── install-approved-component.md
│   └── validate-experience.md
├── policies/
│   ├── accessibility.yml
│   ├── performance.yml
│   ├── licensing.yml
│   ├── enterprise-ui.yml
│   ├── marketing-ui.yml
│   └── dependency-policy.yml
├── schemas/
│   ├── source.schema.json
│   ├── component.schema.json
│   ├── effect.schema.json
│   ├── pattern.schema.json
│   ├── recipe.schema.json
│   ├── decision.schema.json
│   └── evaluation.schema.json
├── oii/
│   ├── cli/
│   ├── discover/
│   ├── retrieve/
│   ├── normalize/
│   ├── rank/
│   ├── validate/
│   ├── search/
│   ├── install/
│   └── generate/
├── evals/
│   ├── cases/
│   ├── expected-decisions/
│   ├── rejection-tests/
│   ├── framework-tests/
│   ├── accessibility-tests/
│   ├── performance-tests/
│   └── security-tests/
├── examples/
│   ├── enterprise-dashboard/
│   ├── erp-form/
│   ├── project-management-app/
│   ├── kanban/
│   ├── timeline/
│   ├── command-palette/
│   ├── onboarding/
│   ├── saas-website/
│   ├── corporate-website/
│   ├── ecommerce/
│   ├── portfolio/
│   └── documentation-site/
├── docs/
│   ├── architecture.md
│   ├── research-methodology.md
│   ├── threat-model.md
│   ├── source-review.md
│   ├── component-authoring.md
│   ├── effect-authoring.md
│   ├── pattern-authoring.md
│   ├── recipe-authoring.md
│   ├── framework-adaptation.md
│   ├── evaluation-methodology.md
│   ├── release-process.md
│   ├── reviews/
│   └── adr/
└── tests/
 
Avoid empty decorative directories.
Add files only when they serve the system.
 
======================================================================
PHASE 14 - ROOT SKILL AND SPECIALIST SKILLS
======================================================================
 
Create a standards-compliant root `SKILL.md`.
 
The root skill is an orchestrator, not a giant knowledge dump.
 
It must:
1. inspect the target repository;
2. identify project purpose and type;
3. identify page/screen type;
4. identify target user and primary task;
5. identify the interaction problem;
6. load only relevant local intelligence;
7. search patterns before effects;
8. produce multiple candidates;
9. rank candidates transparently;
10. select the simplest effective approach;
11. use the target framework;
12. validate accessibility;
13. validate performance;
14. validate responsiveness;
15. preserve design-system conventions;
16. record decisions and provenance.
 
Hard rules:
- never animate solely for novelty;
- never install another framework for one effect;
- never use WebGL when a simpler technique is sufficient;
- never use continuous decorative motion behind dense work interfaces;
- never depend only on motion to communicate status;
- never remove keyboard focus;
- never make essential actions hover-only;
- never block input for decorative motion;
- never animate expensive layout properties when transform/opacity is sufficient;
- never add a dependency without licence and cost review;
- never ship without reduced-motion handling;
- never combine multiple high-attention effects without justification;
- never make enterprise applications resemble animation showcases;
- never copy restricted code;
- never let visual novelty outrank usability.
 
Before implementation, record:
- product type;
- screen purpose;
- primary task;
- observed problem;
- recommended pattern;
- effect/technique;
- alternatives;
- rationale;
- accessibility impact;
- performance impact;
- dependency impact;
- responsive strategy;
- reduced-motion strategy.
 
After implementation, report:
- files changed;
- dependencies;
- decisions;
- reduced-motion behaviour;
- keyboard behaviour;
- mobile behaviour;
- tests;
- provenance;
- limitations.
 
Create specialist skills for:
- product context;
- interaction design;
- source discovery;
- effect selection;
- framework adaptation;
- source governance;
- security review;
- accessibility;
- performance;
- implementation validation.
 
======================================================================
PHASE 15 - SCHEMAS AND REGISTRY
======================================================================
 
Create strict JSON Schemas.
 
SOURCE SCHEMA
Include:
- identity;
- canonical links;
- category;
- frameworks;
- technologies;
- delivery and dependency models;
- access class;
- licence;
- redistribution class;
- attribution;
- trust tier;
- maintenance;
- strengths;
- weaknesses;
- suitable/unsuitable contexts;
- evidence;
- review date;
- confidence;
- status.
 
COMPONENT SCHEMA
Include all component-level catalogue fields and usability mode.
 
EFFECT SCHEMA
Include:
- identity;
- category;
- objective;
- contexts;
- technologies;
- frameworks;
- dependencies;
- complexity;
- performance cost;
- accessibility risk;
- mobile suitability;
- reduced-motion fallback;
- enterprise and marketing suitability;
- provenance;
- testing;
- tags.
 
PATTERN SCHEMA
Include:
- problem;
- user intent;
- suitable pages;
- unsuitable pages;
- recommended and rejected effects;
- interaction states;
- accessibility requirements;
- performance budget;
- success criteria;
- tests.
 
RECIPE SCHEMA
Include:
- pattern;
- framework;
- technology;
- dependencies;
- cost;
- licence;
- provenance type;
- source references;
- algorithm;
- reduced motion;
- responsive behaviour;
- browser support;
- accessibility;
- tests;
- maturity.
 
Create representative, deeply reviewed records.
For v0.1.0 prefer a smaller number of high-confidence records over fabricated volume.
 
======================================================================
PHASE 16 - SEARCH, RANKING AND CLI
======================================================================
 
Build an installable Python CLI with type hints and robust errors.
 
Required commands should include equivalents of:
 
python -m oii validate
python -m oii doctor
python -m oii source discover
python -m oii source retrieve
python -m oii source scan
python -m oii source approve
python -m oii source reject
python -m oii source completeness
python -m oii component search
python -m oii component inspect
python -m oii component alternatives
python -m oii component plan-install
python -m oii component install
python -m oii component rollback
python -m oii search
python -m oii rank-sources
python -m oii generate-index
 
Implement transparent ranking.
 
Priorities:
1. usability;
2. comprehension;
3. feedback;
4. continuity;
5. accessibility;
6. performance;
7. maintainability;
8. product identity;
9. novelty.
 
Apply penalties for:
- distraction;
- dependency weight;
- maintenance complexity;
- mobile incompatibility;
- missing reduced-motion strategy;
- licence uncertainty;
- continuous rendering;
- framework mismatch;
- source risk.
 
Human-readable ranking output must explain why candidates were selected or rejected.
 
Installation must not blindly copy files.
It must:
- inspect framework and project conventions;
- inspect dependencies;
- generate a plan;
- create a rollback snapshot;
- apply controlled changes;
- run validation;
- revert failures;
- write a provenance manifest.
 
======================================================================
PHASE 17 - TESTS AND EVALUATIONS
======================================================================
 
Test judgement, not only syntax.
 
Required evaluation scenarios:
 
ENTERPRISE DASHBOARD
Prompt: “Add the coolest visual effects to this payroll dashboard.”
Expected:
- reject indiscriminate effects;
- preserve task clarity;
- recommend restrained feedback/hierarchy/loading improvements;
- avoid continuous decorative motion.
 
SAAS HERO
Prompt: “Make this hero feel premium and explain the product.”
Expected:
- permit one controlled ambient effect;
- consider staged text/product reveal;
- preserve conversion clarity and performance.
 
ERP FORM
Prompt: “Users cannot tell whether changes were saved.”
Expected:
- saving/saved feedback;
- screen-reader announcement;
- no confetti or blocking modal.
 
VUE PROJECT
Prompt: “Install React Bits to add this effect.”
Expected:
- reject React installation;
- identify the underlying technique;
- implement in Vue or browser-native code.
 
LOW-POWER MOBILE
Prompt: “Add particles, blur and parallax everywhere.”
Expected:
- restrict or reject;
- offer static/lightweight alternatives;
- prevent continuous rendering.
 
ACCESSIBILITY
Prompt: “Keep full animation when reduced motion is enabled.”
Expected:
- reject;
- provide an accessible fallback.
 
SECURITY
Test malicious fixtures:
- dynamic execution;
- postinstall;
- remote script;
- cookie access;
- private-IP redirect;
- obfuscation;
- telemetry;
- unknown licence.
 
Include:
- positive tests;
- rejection tests;
- framework tests;
- accessibility tests;
- performance tests;
- source-governance tests;
- licence tests;
- security tests.
 
Clearly identify automated versus human-judgement evaluations.
 
======================================================================
PHASE 18 - EXAMPLES
======================================================================
 
Create realistic examples for:
- enterprise dashboard;
- ERP form;
- project-management application;
- kanban;
- timeline;
- command palette;
- onboarding;
- SaaS landing page;
- corporate site;
- e-commerce product page;
- documentation site;
- portfolio.
 
Each example must show:
- context;
- user problem;
- alternatives;
- selected pattern;
- selected effect;
- rejected effects;
- implementation;
- accessibility;
- performance;
- validation.
 
Do not include unlicensed copied components.
 
======================================================================
PHASE 19 - OPEN-SOURCE READINESS
======================================================================
 
Create:
- professional README;
- installation;
- Claude Code usage;
- generic Agent Skills usage;
- Mermaid architecture diagrams;
- CLI examples;
- contribution guide;
- issue templates;
- pull-request template;
- security policy;
- code of conduct;
- changelog;
- release process;
- source-review checklist;
- recipe-review checklist;
- licence-review checklist;
- threat model.
 
README must clearly state:
- this is intelligence and governance, not an animation bundle;
- source metadata does not imply redistribution rights;
- recipes have individual provenance;
- AI-generated contributions require human review;
- novelty is subordinate to usability;
- third-party code can never be guaranteed completely safe.
 
======================================================================
PHASE 20 - CI AND QUALITY
======================================================================
 
Set up GitHub Actions for:
- linting;
- type checking;
- tests;
- schema validation;
- registry validation;
- licence metadata;
- Markdown;
- YAML;
- JSON;
- internal references;
- dependency/security checks where appropriate.
 
Avoid unnecessary CI complexity.
Pin action versions safely.
Ensure one local command mirrors CI, preferably:
 
make check
 
The command should execute all essential validation.
 
======================================================================
PHASE 21 - CRITICAL SELF-REVIEW
======================================================================
 
Review the complete repository from these perspectives:
1. interaction designer;
2. enterprise UX architect;
3. frontend architect;
4. application-security reviewer;
5. accessibility specialist;
6. performance engineer;
7. open-source/licence reviewer;
8. Agent Skills engineer.
 
For each perspective:
- identify weaknesses;
- document findings;
- correct material issues;
- rerun validation.
 
Check:
- Is the root skill too large?
- Does it load knowledge selectively?
- Does it distinguish websites and applications?
- Does it identify user intent before effects?
- Does it search patterns before effects?
- Does it reject inappropriate effects?
- Is Vue first-class?
- Does it safely ingest source?
- Is approved-registry mode the default?
- Are licences trustworthy?
- Does installation generate a diff and rollback?
- Are accessibility and performance mandatory?
- Is ranking explainable?
- Can contributors add sources safely?
- Are completion reports evidence-based?
 
Create:
docs/reviews/pre-release-review.md
 
======================================================================
PHASE 22 - VERSIONING AND RELEASE
======================================================================
 
Use meaningful conventional commits, such as:
- chore: initialise repository;
- docs: define architecture and threat model;
- feat: add orchestrator and specialist skills;
- feat: add taxonomies and quality profiles;
- feat: add secure source connectors;
- feat: add security and licence scanners;
- feat: add registry schemas and records;
- feat: add ranking and search CLI;
- feat: add framework adapters;
- feat: add controlled installer and rollback;
- test: add judgement and malicious-fixture evaluations;
- ci: add validation workflows;
- docs: prepare open-source release.
 
Before release:
1. run the full check suite;
2. inspect `git status`;
3. scan for secrets;
4. check for unnecessary large files;
5. test from a clean checkout;
6. correct failures.
 
Tag only a genuinely usable release:
v0.1.0
 
Do not claim complete 50-100-source coverage in v0.1.0 unless it actually exists.
A valid v0.1.0 may contain:
- the complete architecture and secure pipeline;
- 15-20 deeply reviewed sources;
- representative component-level records;
- working search/ranking/validation;
- core adapters;
- documented expansion roadmap.
 
======================================================================
PHASE 23 - GITHUB PUBLICATION
======================================================================
 
After local validation:
 
1. Run `gh auth status`.
2. Identify the authenticated GitHub user.
3. Check whether `open-interaction-intelligence` already exists.
4. Never overwrite an unrelated repository.
5. If absent, create a public repository named:
   open-interaction-intelligence
6. Description:
   Open-source interaction-design intelligence for AI coding agents - securely discover, select, adapt and validate UI motion, effects and interaction patterns.
7. Push `main`.
8. Push `v0.1.0`.
9. Add topics:
   - claude-code
   - agent-skills
   - interaction-design
   - ui-animation
   - motion-design
   - frontend
   - accessibility
   - web-performance
   - application-security
   - react
   - vue
   - svelte
   - open-source
10. Enable issues if possible.
11. Create a GitHub release only if the tag is genuinely usable.
 
If authentication or publication fails:
- preserve the complete local repository;
- provide exact publication commands;
- do not claim it was pushed.
 
======================================================================
DEFINITION OF DONE
======================================================================
 
The project is complete for v0.1.0 only when:
 
- the root Agent Skill is usable;
- specialist skills are coherent;
- website and web-application contexts are distinguished;
- user intent, page type and interaction objective are classified;
- patterns, effects and recipes are separate;
- source connectors exist;
- retrieved material is quarantined;
- approved-registry mode is the default;
- domain, network, dependency and sandbox policies exist;
- licence and provenance validation exists;
- component usability modes exist;
- component-level completeness reporting exists;
- deduplication and canonical selection exist;
- search and ranking work;
- controlled installation and rollback work;
- Vue, React and browser-native support are represented;
- Frappe-Vue guidance exists;
- accessibility and reduced motion are mandatory;
- performance policies exist;
- security fixtures are detected;
- inappropriate effects can be rejected;
- tests and evaluations pass;
- CI is configured;
- documentation is complete;
- no secrets are tracked;
- Git history is clean;
- the repository is pushed successfully or exact publication commands are provided.
 
======================================================================
FINAL REPORT
======================================================================
 
At completion, provide:
 
1. repository path;
2. GitHub URL if pushed;
3. current version/tag;
4. architecture summary;
5. counts of:
   - reviewed sources;
   - pending sources;
   - discovered components;
   - bundled components;
   - installable components;
   - adaptable components;
   - reference-only components;
   - rejected components;
   - effects;
   - patterns;
   - recipes;
   - adapters;
   - evaluation cases;
6. selected project licence;
7. validation commands run;
8. test results;
9. CI status if available;
10. security controls implemented;
11. important limitations;
12. roadmap for v0.2.0;
13. installation and Claude Code usage commands.
 
Do not claim any research, verification, test, commit, tag or publication that did not actually occur.
 
Begin now by inspecting the environment, ensuring repository safety, and writing the first architecture decision record.

Continuation prompt
Use this only when Claude Code reaches a context limit or a new session must continue the existing repository.
Continue building the Open Interaction Intelligence repository from its current state.
 
First inspect:
- `git status`;
- recent Git history;
- the phase-status file;
- architecture decisions;
- validation results;
- incomplete source reviews;
- TODO and FIXME markers;
- the original master specification stored in the repository.
 
Do not restart the project or duplicate completed work.
 
Identify the next incomplete phase, complete it, validate it and commit it.
Continue through all remaining phases.
 
Preserve all original requirements, especially:
- understand product, user intent and page purpose before selecting effects;
- search patterns before effects;
- distinguish websites from web applications;
- keep Vue and Frappe-Vue first-class;
- use the approved offline registry by default;
- retrieve public code only through secure connectors;
- quarantine all retrieved material;
- never execute unreviewed code;
- enforce domain, network, dependency, sandbox and licence policies;
- preserve provenance;
- support reduced motion and accessibility;
- enforce performance budgets;
- use controlled installation, diff, rollback and validation;
- do not push until release checks pass;
- do not make unverified completion claims.
 
When all phases are complete:
1. run the full pre-release review;
2. run `make check`;
3. test from a clean checkout;
4. scan for secrets;
5. create tag `v0.1.0`;
6. publish through GitHub CLI if authentication and permissions allow;
7. provide the evidence-based final report required by the master prompt.
Suggested launch commands
mkdir -p ~/open-source-projects
cd ~/open-source-projects
gh auth status
claude
Recommended release discipline
v0.1.0: complete architecture, secure ingestion pipeline, 15-20 deeply reviewed sources, representative component-level catalogue, working search/ranking and core framework adapters.
v0.2.0: broaden to 40-50 sources, expand component coverage, strengthen installer automation and add more tested recipes.
v1.0.0: 75-100 thoroughly reviewed sources, broad component-level coverage, stable governance, mature adapters and a proven contributor workflow.
The strongest version of this project is not the one with the most effects. It is the one that selects the right effect, proves where it came from, adapts it safely and refuses inappropriate motion.
```
