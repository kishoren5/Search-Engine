"""Interactive Single-Page Application for the BFSI Sentinel Financial Intelligence Platform."""

FINTECH_UI_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BFSI Sentinel — Financial Intelligence & Search Engine Command Center</title>
  <style>
    :root {
      --bg-primary: #060912;
      --bg-secondary: #0b1120;
      --bg-card: rgba(15, 23, 42, 0.85);
      --bg-card-hover: rgba(24, 35, 60, 0.95);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(56, 189, 248, 0.5);
      --accent-blue: #0284c7;
      --accent-cyan: #38bdf8;
      --accent-gold: #f59e0b;
      --accent-emerald: #10b981;
      --accent-crimson: #ef4444;
      --accent-purple: #8b5cf6;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --font-mono: 'Consolas', 'Courier New', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg-primary);
      color: var(--text-main);
      font-family: var(--font-family);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Header */
    header {
      background: linear-gradient(180deg, rgba(11, 17, 32, 0.98) 0%, rgba(6, 9, 18, 0.94) 100%);
      border-bottom: 1px solid var(--border-color);
      padding: 0.85rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(14px);
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .brand-icon {
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, var(--accent-blue), #4f46e5);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.2rem;
      color: #fff;
      box-shadow: 0 0 20px rgba(2, 132, 199, 0.45);
    }

    .brand-title {
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .brand-tag {
      font-size: 0.68rem;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-cyan);
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      border: 1px solid rgba(56, 189, 248, 0.3);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-left: 0.5rem;
    }

    /* Navigation Tabs */
    .nav-tabs {
      display: flex;
      gap: 0.35rem;
      background: rgba(255, 255, 255, 0.03);
      padding: 0.3rem;
      border-radius: 10px;
      border: 1px solid var(--border-color);
    }

    .nav-tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }

    .nav-tab-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }

    .nav-tab-btn.active {
      background: linear-gradient(135deg, var(--accent-blue), #2563eb);
      color: #fff;
      box-shadow: 0 2px 10px rgba(2, 132, 199, 0.4);
    }

    .header-actions {
      display: flex;
      gap: 0.75rem;
      align-items: center;
    }

    .badge {
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.8rem;
    }

    .indicator-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: var(--accent-emerald);
      box-shadow: 0 0 8px var(--accent-emerald);
    }

    .btn-locker {
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: var(--accent-gold);
      padding: 0.35rem 0.85rem;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .btn-locker:hover {
      background: rgba(245, 158, 11, 0.25);
    }

    /* Main Container */
    main {
      flex: 1;
      max-width: 1440px;
      margin: 0 auto;
      padding: 1.75rem 1.5rem;
      width: 100%;
    }

    .tab-content { display: none; }
    .tab-content.active { display: block; }

    /* Panels */
    .panel-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.75rem;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(12px);
      margin-bottom: 1.75rem;
    }

    /* Search Bar */
    .search-input-wrapper {
      position: relative;
      display: flex;
      gap: 0.75rem;
    }

    .search-input {
      flex: 1;
      background: rgba(6, 9, 18, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 10px;
      padding: 0.95rem 1.25rem;
      color: #fff;
      font-size: 1.05rem;
      outline: none;
      transition: all 0.2s ease;
    }

    .search-input:focus {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25);
    }

    .btn-action {
      background: linear-gradient(135deg, var(--accent-blue), #2563eb);
      color: white;
      border: none;
      border-radius: 10px;
      padding: 0 1.75rem;
      font-weight: 600;
      font-size: 0.95rem;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      white-space: nowrap;
    }

    .btn-action:hover {
      background: linear-gradient(135deg, #0284c7, #1d4ed8);
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    }

    .btn-success {
      background: linear-gradient(135deg, #10b981, #059669);
      box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
    }
    .btn-success:hover {
      background: linear-gradient(135deg, #059669, #047857);
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.55rem 1rem;
      border-radius: 8px;
      font-size: 0.82rem;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }
    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: var(--border-focus);
    }

    /* Preset Chips */
    .chips-group {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1rem;
      align-items: center;
    }

    .chips-label {
      font-size: 0.74rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-right: 0.25rem;
      font-weight: 700;
    }

    .chip-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      font-size: 0.78rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .chip-btn:hover {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--accent-cyan);
      color: var(--text-main);
    }

    .chip-btn.active {
      background: rgba(56, 189, 248, 0.25);
      border-color: var(--accent-cyan);
      color: #fff;
      font-weight: 700;
    }

    /* Algorithm Preset & Sliders Bar */
    .tuning-row {
      display: flex;
      gap: 1.5rem;
      margin-top: 1.25rem;
      padding: 1rem 1.25rem;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.06);
      align-items: center;
      flex-wrap: wrap;
    }

    .slider-group {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-size: 0.85rem;
    }

    .slider-group label {
      color: var(--text-muted);
      font-weight: 600;
      white-space: nowrap;
    }

    .slider-group input[type="range"] {
      width: 110px;
      accent-color: var(--accent-cyan);
      cursor: pointer;
    }

    .slider-val {
      font-family: var(--font-mono);
      color: var(--accent-cyan);
      font-weight: 700;
      min-width: 32px;
    }

    /* Interactive Filters Bar */
    .filters-bar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      margin-top: 1.25rem;
      padding-top: 1.25rem;
      border-top: 1px solid var(--border-color);
    }

    .filter-item {
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }

    .filter-item label {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      font-weight: 700;
    }

    .filter-select, .input-text {
      background: rgba(6, 9, 18, 0.85);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.55rem 0.75rem;
      border-radius: 8px;
      font-size: 0.85rem;
      outline: none;
      cursor: pointer;
    }

    .filter-select:focus, .input-text:focus {
      border-color: var(--accent-cyan);
    }

    /* Waterfall Widget */
    .waterfall-card {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1rem 1.25rem;
      margin-bottom: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    .waterfall-bar {
      display: flex;
      height: 12px;
      border-radius: 6px;
      overflow: hidden;
      background: rgba(255, 255, 255, 0.05);
      width: 100%;
    }

    .wf-seg { height: 100%; transition: width 0.3s ease; }
    .wf-tokenize { background-color: #38bdf8; }
    .wf-retrieval { background-color: #10b981; }
    .wf-explain { background-color: #f59e0b; }
    .wf-hydration { background-color: #8b5cf6; }

    .waterfall-legend {
      display: flex;
      gap: 1.5rem;
      font-size: 0.78rem;
      color: var(--text-muted);
      flex-wrap: wrap;
    }

    .legend-item { display: flex; align-items: center; gap: 0.4rem; }
    .legend-color { width: 10px; height: 10px; border-radius: 3px; }

    /* Results Header & Actions */
    .results-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      font-size: 0.88rem;
      color: var(--text-muted);
    }

    .results-actions {
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }

    /* Result Cards */
    .results-grid {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .result-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      transition: all 0.2s ease;
      position: relative;
    }

    .result-card:hover {
      border-color: rgba(56, 189, 248, 0.45);
      transform: translateY(-2px);
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
    }

    .card-meta-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.6rem;
      font-size: 0.8rem;
    }

    .badges-cluster {
      display: flex;
      gap: 0.5rem;
      align-items: center;
      flex-wrap: wrap;
    }

    .risk-badge {
      font-weight: 800;
      font-size: 0.7rem;
      padding: 0.18rem 0.55rem;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .risk-CRITICAL { background: rgba(239, 68, 68, 0.22); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .risk-HIGH { background: rgba(245, 158, 11, 0.22); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .risk-MEDIUM { background: rgba(56, 189, 248, 0.22); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.4); }
    .risk-LOW { background: rgba(16, 185, 129, 0.22); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.4); }

    .type-badge {
      background: rgba(255, 255, 255, 0.07);
      color: var(--text-muted);
      padding: 0.18rem 0.55rem;
      border-radius: 4px;
      font-size: 0.7rem;
      border: 1px solid var(--border-color);
      font-weight: 600;
    }

    .ticker-chip {
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.22), rgba(99, 102, 241, 0.22));
      color: #93c5fd;
      padding: 0.18rem 0.55rem;
      border-radius: 4px;
      font-weight: 700;
      font-size: 0.72rem;
      border: 1px solid rgba(147, 197, 253, 0.3);
    }

    .score-meter-wrap {
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    .score-bar-bg {
      width: 70px;
      height: 6px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 3px;
      overflow: hidden;
    }

    .score-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
    }

    .card-title {
      font-size: 1.15rem;
      font-weight: 600;
      color: #fff;
      margin-bottom: 0.45rem;
      line-height: 1.35;
    }

    .highlight-term {
      background: rgba(56, 189, 248, 0.22);
      color: #38bdf8;
      padding: 0.05rem 0.25rem;
      border-radius: 3px;
      font-weight: 600;
    }

    .card-snippet {
      font-size: 0.92rem;
      color: #cbd5e1;
      margin-bottom: 0.85rem;
      line-height: 1.55;
    }

    .card-meta-bottom {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.78rem;
      color: var(--text-muted);
      padding-top: 0.65rem;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
    }

    .amount-highlight {
      font-family: var(--font-mono);
      color: var(--accent-gold);
      font-weight: 700;
      font-size: 0.85rem;
    }

    .card-tools {
      display: flex;
      gap: 0.5rem;
      align-items: center;
    }

    /* Explanation Math Drawer */
    .explain-box {
      margin: 0.75rem 0;
      padding: 0.75rem 1rem;
      background: rgba(0, 0, 0, 0.35);
      border-radius: 8px;
      border: 1px dashed rgba(56, 189, 248, 0.3);
      font-size: 0.8rem;
    }

    .explain-table {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-mono);
      margin-top: 0.4rem;
    }

    .explain-table th, .explain-table td {
      padding: 0.3rem 0.5rem;
      text-align: left;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .explain-table th { color: var(--text-muted); font-size: 0.72rem; }

    /* A/B Comparison Layout */
    .ab-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }

    .delta-badge {
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      margin-left: 0.4rem;
    }
    .delta-up { background: rgba(16, 185, 129, 0.22); color: #34d399; }
    .delta-down { background: rgba(239, 68, 68, 0.22); color: #f87171; }
    .delta-same { background: rgba(255, 255, 255, 0.08); color: var(--text-muted); }
    .delta-new { background: rgba(56, 189, 248, 0.22); color: #38bdf8; }

    /* Test Cards */
    .test-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 1.25rem;
      margin-bottom: 1.5rem;
    }

    .test-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.25rem;
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .test-card:hover {
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-2px);
    }

    .test-status-pill {
      font-size: 0.72rem;
      font-weight: 800;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .status-PASSED { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .status-FAILED { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .status-IDLE { background: rgba(255, 255, 255, 0.06); color: var(--text-muted); border: 1px solid var(--border-color); }
    .status-RUNNING { background: rgba(56, 189, 248, 0.2); color: var(--accent-cyan); border: 1px solid var(--accent-cyan); animation: pulse 1s infinite alternate; }

    @keyframes pulse { from { opacity: 0.6; } to { opacity: 1; } }

    /* Terminal Console */
    .terminal-window {
      background: #040711;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .terminal-header {
      background: #0a0f1d;
      padding: 0.5rem 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      border-bottom: 1px solid var(--border-color);
      font-size: 0.75rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    .terminal-body {
      padding: 1.25rem;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: #e2e8f0;
      min-height: 160px;
      max-height: 280px;
      overflow-y: auto;
      white-space: pre-wrap;
      line-height: 1.6;
    }

    /* KPI Grid */
    .stats-kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 1rem;
      margin-bottom: 1.25rem;
    }

    .kpi-tile {
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1rem;
      text-align: center;
    }

    .kpi-tile-label {
      font-size: 0.72rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
    }

    .kpi-tile-val {
      font-size: 1.45rem;
      font-weight: 800;
      font-family: var(--font-mono);
      margin-top: 0.2rem;
      color: var(--accent-cyan);
    }

    /* Evidence Drawer */
    .drawer-overlay {
      position: fixed;
      top: 0; right: 0; bottom: 0; width: 440px;
      background: #0c1222;
      border-left: 1px solid rgba(56, 189, 248, 0.3);
      box-shadow: -10px 0 40px rgba(0, 0, 0, 0.8);
      z-index: 100;
      transform: translateX(100%);
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      flex-direction: column;
      padding: 1.5rem;
    }

    .drawer-overlay.active {
      transform: translateX(0);
    }

    /* Modal */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 100;
      padding: 1.5rem;
    }
    .modal-overlay.active { display: flex; }

    .modal-card {
      background: #0e1526;
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 16px;
      max-width: 800px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 2rem;
      position: relative;
    }

    .empty-state {
      text-align: center;
      padding: 3rem 2rem;
      color: var(--text-muted);
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">BF</div>
      <div>
        <span class="brand-title">BFSI Sentinel</span>
        <span class="brand-tag">Zero-Copy MMAP Engine</span>
      </div>
    </div>

    <nav class="nav-tabs">
      <button class="nav-tab-btn active" onclick="switchTab('searchTab', this)">🔍 Search & Live Tuner</button>
      <button class="nav-tab-btn" onclick="switchTab('abTab', this)">⚖️ A/B Comparison</button>
      <button class="nav-tab-btn" onclick="switchTab('testTab', this)">🧪 Test Harness</button>
      <button class="nav-tab-btn" onclick="switchTab('benchTab', this)">⚡ Concurrency Bench</button>
      <button class="nav-tab-btn" onclick="switchTab('ingestTab', this)">📝 Live Ingest</button>
      <button class="nav-tab-btn" onclick="switchTab('inspectTab', this)">📦 Lexicon & Segments</button>
    </nav>

    <div class="header-actions">
      <div class="badge">
        <span class="indicator-dot"></span>
        <span>Engine: <strong id="headerStatus">ONLINE</strong></span>
      </div>
      <div class="badge">
        <span>Corpus: <strong id="headerDocs">50,000 Records</strong></span>
      </div>
      <button class="btn-locker" onclick="toggleEvidenceLocker()">
        <span>⭐ Evidence Locker:</span>
        <strong id="lockerCount">0</strong>
      </button>
    </div>
  </header>

  <main>
    <!-- TAB 1: SEARCH & LIVE TUNER -->
    <section id="searchTab" class="tab-content active">
      <div class="panel-card">
        <div class="search-input-wrapper">
          <input 
            type="text" 
            id="queryInput" 
            class="search-input" 
            placeholder="Type any search query (e.g. suspicious cash structuring smurfing CTR)..." 
            value="suspicious cash structuring smurfing CTR"
            oninput="handleLiveSearch()"
            autofocus
          />
          <button class="btn-action" onclick="executeSearch()">
            <span>Execute Search</span>
          </button>
        </div>

        <!-- Scenario Quick Presets -->
        <div class="chips-group">
          <span class="chips-label">Scenario Presets:</span>
          <button class="chip-btn" onclick="applyPreset('suspicious cash structuring smurfing CTR', 'CRITICAL', '', '')">AML Structuring (Critical)</button>
          <button class="chip-btn" onclick="applyPreset('Basel III CET1 capital adequacy ratio', '', 'JPM', 'SEC_FILING')">JPMorgan Basel III (10-K)</button>
          <button class="chip-btn" onclick="applyPreset('gross notional derivative credit default swap CDS', '', 'GS', '')">Goldman Sachs CDS Exposure</button>
          <button class="chip-btn" onclick="applyPreset('SWIFT MT103 foreign exchange spot CLS settlement', '', '', 'SWIFT_TX')">SWIFT FX Settlement</button>
          <button class="chip-btn" onclick="applyPreset('commercial real estate non-performing loans NPL', 'HIGH', 'BAC', '')">BAC CRE Non-Performing Loans</button>
          <button class="chip-btn" onclick="applyPreset('privacy mixer cryptocurrency off-ramp layering', 'CRITICAL', '', 'AML_SAR')">Crypto Mixer Layering</button>
        </div>

        <!-- Algorithm Presets & BM25 Sliders -->
        <div class="tuning-row">
          <div style="display:flex; gap:0.4rem; align-items:center;">
            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Algorithm Presets:</span>
            <button class="btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.6rem;" onclick="setBm25Preset(1.2, 0.75)">Lucene Standard</button>
            <button class="btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.6rem;" onclick="setBm25Preset(2.0, 0.75)">High Saturation</button>
            <button class="btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.6rem;" onclick="setBm25Preset(1.2, 0.90)">Short Doc Boost</button>
            <button class="btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.6rem;" onclick="setBm25Preset(1.2, 0.0)">No Length Penalty</button>
          </div>

          <div class="slider-group">
            <label for="k1Slider">k₁ (Saturation):</label>
            <input type="range" id="k1Slider" min="0.1" max="2.5" step="0.05" value="1.2" oninput="updateSliders()"/>
            <span id="k1Val" class="slider-val">1.2</span>
          </div>

          <div class="slider-group">
            <label for="bSlider">b (Penalty):</label>
            <input type="range" id="bSlider" min="0.0" max="1.0" step="0.05" value="0.75" oninput="updateSliders()"/>
            <span id="bVal" class="slider-val">0.75</span>
          </div>

          <label style="display:flex; align-items:center; gap:0.4rem; font-size:0.85rem; cursor:pointer; margin-left:auto;">
            <input type="checkbox" id="explainToggle" checked onchange="executeSearch()" style="accent-color:var(--accent-emerald);" />
            <span>Term Score Breakdown</span>
          </label>
        </div>

        <!-- Filter Chips & Dropdowns -->
        <div class="filters-bar">
          <div class="filter-item">
            <label for="tickerFilter">Institution / Ticker</label>
            <select id="tickerFilter" class="filter-select" onchange="executeSearch()">
              <option value="">All Institutions</option>
              <option value="JPM">JPMorgan Chase (JPM)</option>
              <option value="GS">Goldman Sachs (GS)</option>
              <option value="MS">Morgan Stanley (MS)</option>
              <option value="BAC">Bank of America (BAC)</option>
              <option value="C">Citigroup (C)</option>
              <option value="WFC">Wells Fargo (WFC)</option>
              <option value="BNP">BNP Paribas (BNP)</option>
              <option value="DB">Deutsche Bank (DB)</option>
              <option value="HSBC">HSBC Holdings (HSBC)</option>
              <option value="BARC">Barclays (BARC)</option>
            </select>
          </div>

          <div class="filter-item">
            <label for="riskFilter">Risk Severity</label>
            <select id="riskFilter" class="filter-select" onchange="executeSearch()">
              <option value="">All Risk Tiers</option>
              <option value="CRITICAL">Critical Severity</option>
              <option value="HIGH">High Risk</option>
              <option value="MEDIUM">Medium Risk</option>
              <option value="LOW">Low Risk</option>
            </select>
          </div>

          <div class="filter-item">
            <label for="docTypeFilter">Regulatory Archetype</label>
            <select id="docTypeFilter" class="filter-select" onchange="executeSearch()">
              <option value="">All Record Types</option>
              <option value="AML_SAR">AML / SAR Alert</option>
              <option value="SEC_FILING">SEC 10-K / 10-Q Filing</option>
              <option value="SWIFT_TX">SWIFT MT103 Interbank</option>
              <option value="CREDIT_UNDERWRITING">Credit Underwriting</option>
            </select>
          </div>

          <div class="filter-item">
            <label for="jurisdictionFilter">Jurisdiction</label>
            <select id="jurisdictionFilter" class="filter-select" onchange="executeSearch()">
              <option value="">All Jurisdictions</option>
              <option value="US">United States (US)</option>
              <option value="EU">European Union (EU)</option>
              <option value="UK">United Kingdom (UK)</option>
              <option value="CH">Switzerland (CH)</option>
              <option value="SG">Singapore (SG)</option>
              <option value="HK">Hong Kong (HK)</option>
            </select>
          </div>

          <div class="filter-item">
            <label for="limitFilter">Candidates Limit</label>
            <select id="limitFilter" class="filter-select" onchange="executeSearch()">
              <option value="10">Top 10 Hits</option>
              <option value="25">Top 25 Hits</option>
              <option value="50">Top 50 Hits</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Zero-Copy Latency Waterfall -->
      <div id="waterfallCard" class="waterfall-card">
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.82rem;">
          <span>⚡ <strong>Zero-Copy Memory-Mapped Execution Waterfall:</strong> <span id="wfTotalMs" style="color:var(--accent-cyan); font-weight:700;">-- ms</span></span>
          <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted);">OS Page Cache Hit — Direct Virtual Memory</span>
        </div>
        <div class="waterfall-bar">
          <div id="wfTokenizeBar" class="wf-seg wf-tokenize" style="width: 15%;" title="Tokenization"></div>
          <div id="wfRetrievalBar" class="wf-seg wf-retrieval" style="width: 50%;" title="MMap & Postings Retrieval"></div>
          <div id="wfExplainBar" class="wf-seg wf-explain" style="width: 20%;" title="Math Breakdown"></div>
          <div id="wfHydrationBar" class="wf-seg wf-hydration" style="width: 15%;" title="Hydration"></div>
        </div>
        <div class="waterfall-legend">
          <div class="legend-item"><span class="legend-color wf-tokenize"></span><span>Tokenize: <strong id="wfTokenizeVal">--</strong></span></div>
          <div class="legend-item"><span class="legend-color wf-retrieval"></span><span>MMap Postings: <strong id="wfRetrievalVal">--</strong></span></div>
          <div class="legend-item"><span class="legend-color wf-explain"></span><span>Math Breakdown: <strong id="wfExplainVal">--</strong></span></div>
          <div class="legend-item"><span class="legend-color wf-hydration"></span><span>Hydration: <strong id="wfHydrationVal">--</strong></span></div>
        </div>
      </div>

      <!-- Results Header -->
      <div class="results-header">
        <span id="resultsCount">Ready to search.</span>
        <div class="results-actions">
          <button class="btn-secondary" onclick="exportResultsJson()">Export JSON</button>
          <button class="btn-secondary" onclick="exportResultsCsv()">Export CSV</button>
        </div>
      </div>

      <!-- Results List -->
      <div id="resultsGrid" class="results-grid"></div>
    </section>

    <!-- TAB 2: A/B COMPARISON STUDIO -->
    <section id="abTab" class="tab-content">
      <div class="panel-card">
        <h2 style="font-size:1.25rem; margin-bottom:0.5rem;">⚖️ A/B Search & Ranking Experimentation Studio</h2>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1.25rem;">Compare two ranking algorithms, query variations, or filter policies simultaneously with automated per-document rank delta calculations.</p>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.5rem; margin-bottom:1.25rem;">
          <div style="background:rgba(0,0,0,0.3); padding:1rem; border-radius:10px; border:1px solid var(--border-color);">
            <div style="font-size:0.8rem; font-weight:700; color:var(--accent-cyan); text-transform:uppercase; margin-bottom:0.5rem;">Config A (Baseline)</div>
            <input type="text" id="abQueryA" class="search-input" style="width:100%; margin-bottom:0.75rem;" value="suspicious cash structuring smurfing CTR" />
            <div style="display:flex; gap:1rem; font-size:0.82rem;">
              <span>k₁: <strong id="abValK1A">1.2</strong></span>
              <input type="range" id="abSliderK1A" min="0.1" max="2.5" step="0.1" value="1.2" oninput="document.getElementById('abValK1A').textContent=this.value;" />
              <span>b: <strong id="abValBA">0.75</strong></span>
              <input type="range" id="abSliderBA" min="0.0" max="1.0" step="0.05" value="0.75" oninput="document.getElementById('abValBA').textContent=this.value;" />
            </div>
          </div>

          <div style="background:rgba(0,0,0,0.3); padding:1rem; border-radius:10px; border:1px solid rgba(139, 92, 246, 0.4);">
            <div style="font-size:0.8rem; font-weight:700; color:var(--accent-purple); text-transform:uppercase; margin-bottom:0.5rem;">Config B (Variant)</div>
            <input type="text" id="abQueryB" class="search-input" style="width:100%; margin-bottom:0.75rem;" value="suspicious cash structuring smurfing CTR" />
            <div style="display:flex; gap:1rem; font-size:0.82rem;">
              <span>k₁: <strong id="abValK1B">2.0</strong></span>
              <input type="range" id="abSliderK1B" min="0.1" max="2.5" step="0.1" value="2.0" oninput="document.getElementById('abValK1B').textContent=this.value;" />
              <span>b: <strong id="abValBB">0.30</strong></span>
              <input type="range" id="abSliderBB" min="0.0" max="1.0" step="0.05" value="0.3" oninput="document.getElementById('abValBB').textContent=this.value;" />
            </div>
          </div>
        </div>

        <button class="btn-action" style="width:100%; justify-content:center; padding:0.85rem;" onclick="executeAbComparison()">
          🚀 Run Simultaneous A/B Experiment
        </button>
      </div>

      <div class="ab-grid">
        <div>
          <div style="background:rgba(0,0,0,0.3); padding:0.6rem 1rem; border-radius:8px; border:1px solid var(--border-color); display:flex; justify-content:space-between; margin-bottom:1rem; font-size:0.85rem;">
            <strong>Config A Hits</strong>
            <span id="abTimeA">-- ms</span>
          </div>
          <div id="abResultsA" class="results-grid"></div>
        </div>

        <div>
          <div style="background:rgba(0,0,0,0.3); padding:0.6rem 1rem; border-radius:8px; border:1px solid rgba(139,92,246,0.4); display:flex; justify-content:space-between; margin-bottom:1rem; font-size:0.85rem;">
            <strong style="color:var(--accent-purple);">Config B Hits</strong>
            <span id="abTimeB">-- ms</span>
          </div>
          <div id="abResultsB" class="results-grid"></div>
        </div>
      </div>
    </section>

    <!-- TAB 3: AUTOMATED TEST HARNESS -->
    <section id="testTab" class="tab-content">
      <div class="panel-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;">
          <div>
            <h2 style="font-size:1.25rem; margin-bottom:0.25rem;">🧪 In-Engine Automated Verification Suite</h2>
            <p style="font-size:0.85rem; color:var(--text-muted);">Execute bit-level codec validation, SEC Rule 17a-4 audit, zero-copy concurrency checks, and BM25 monotonicity directly in the browser.</p>
          </div>
          <button id="btnRunSuite" class="btn-action btn-success" onclick="runFullTestSuite()">
            <span>🚀 Run Full Test Suite</span>
          </button>
        </div>

        <!-- Progress Bar -->
        <div id="testProgressWrap" style="display:none; height:8px; background:rgba(255,255,255,0.06); border-radius:4px; overflow:hidden; margin-bottom:1.5rem;">
          <div id="testProgressBar" style="width:0%; height:100%; background:linear-gradient(90deg, #38bdf8, #10b981); transition:width 0.3s ease;"></div>
        </div>

        <div class="test-cards-grid">
          <!-- TC-01 -->
          <div class="test-card" onclick="toggleTestLog('logTC01')">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <strong style="font-size:0.95rem;">TC-01: VByte 7-Bit Delta Codec</strong>
              <span id="statusTC01" class="test-status-pill status-IDLE">IDLE</span>
            </div>
            <p id="sumTC01" style="font-size:0.82rem; color:var(--text-muted);">5,000 synthetic values round-trip compression and decompression validation.</p>
            <div id="logTC01" style="display:none; margin-top:0.75rem; padding:0.6rem; background:rgba(0,0,0,0.4); border-radius:6px; font-family:var(--font-mono); font-size:0.75rem; color:#93c5fd;"></div>
          </div>

          <!-- TC-02 -->
          <div class="test-card" onclick="toggleTestLog('logTC02')">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <strong style="font-size:0.95rem;">TC-02: SEC Rule 17a-4 SHA-256 Audit</strong>
              <span id="statusTC02" class="test-status-pill status-IDLE">IDLE</span>
            </div>
            <p id="sumTC02" style="font-size:0.82rem; color:var(--text-muted);">Cryptographic checksum integrity verification across segment manifest artifacts.</p>
            <div id="logTC02" style="display:none; margin-top:0.75rem; padding:0.6rem; background:rgba(0,0,0,0.4); border-radius:6px; font-family:var(--font-mono); font-size:0.75rem; color:#93c5fd;"></div>
          </div>

          <!-- TC-03 -->
          <div class="test-card" onclick="toggleTestLog('logTC03')">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <strong style="font-size:0.95rem;">TC-03: Zero-Copy MMap Concurrency</strong>
              <span id="statusTC03" class="test-status-pill status-IDLE">IDLE</span>
            </div>
            <p id="sumTC03" style="font-size:0.82rem; color:var(--text-muted);">64 parallel reads across 16 worker threads with zero buffer contention.</p>
            <div id="logTC03" style="display:none; margin-top:0.75rem; padding:0.6rem; background:rgba(0,0,0,0.4); border-radius:6px; font-family:var(--font-mono); font-size:0.75rem; color:#93c5fd;"></div>
          </div>

          <!-- TC-04 -->
          <div class="test-card" onclick="toggleTestLog('logTC04')">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <strong style="font-size:0.95rem;">TC-04: BM25 Scoring Monotonicity</strong>
              <span id="statusTC04" class="test-status-pill status-IDLE">IDLE</span>
            </div>
            <p id="sumTC04" style="font-size:0.82rem; color:var(--text-muted);">Mathematical monotonicity and min-heap ordering invariant assertion.</p>
            <div id="logTC04" style="display:none; margin-top:0.75rem; padding:0.6rem; background:rgba(0,0,0,0.4); border-radius:6px; font-family:var(--font-mono); font-size:0.75rem; color:#93c5fd;"></div>
          </div>

          <!-- TC-05 -->
          <div class="test-card" onclick="toggleTestLog('logTC05')">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <strong style="font-size:0.95rem;">TC-05: Regulatory Filter Isolation</strong>
              <span id="statusTC05" class="test-status-pill status-IDLE">IDLE</span>
            </div>
            <p id="sumTC05" style="font-size:0.82rem; color:var(--text-muted);">Strict isolation across risk, ticker, and regulatory archetype boundaries.</p>
            <div id="logTC05" style="display:none; margin-top:0.75rem; padding:0.6rem; background:rgba(0,0,0,0.4); border-radius:6px; font-family:var(--font-mono); font-size:0.75rem; color:#93c5fd;"></div>
          </div>

          <!-- TC-06 -->
          <div class="test-card" onclick="toggleTestLog('logTC06')">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <strong style="font-size:0.95rem;">TC-06: Golden IR Benchmark (MRR)</strong>
              <span id="statusTC06" class="test-status-pill status-IDLE">IDLE</span>
            </div>
            <p id="sumTC06" style="font-size:0.82rem; color:var(--text-muted);">Mean Reciprocal Rank on golden financial compliance queries (Target >= 0.80).</p>
            <div id="logTC06" style="display:none; margin-top:0.75rem; padding:0.6rem; background:rgba(0,0,0,0.4); border-radius:6px; font-family:var(--font-mono); font-size:0.75rem; color:#93c5fd;"></div>
          </div>
        </div>

        <!-- Terminal Console -->
        <div class="terminal-window">
          <div class="terminal-header">
            <span>● Test Execution Live Stream Console</span>
          </div>
          <div id="testLogTerminal" class="terminal-body">BFSI Sentinel Test Runner Ready. Click 'Run Full Test Suite' to begin automated verification.</div>
        </div>
      </div>
    </section>

    <!-- TAB 4: CONCURRENCY STRESS TESTER -->
    <section id="benchTab" class="tab-content">
      <div style="display:grid; grid-template-columns: 340px 1fr; gap:1.5rem;">
        <div class="panel-card">
          <h3 style="font-size:1.1rem; color:#fff; margin-bottom:1.25rem;">⚡ Load Parameters</h3>
          
          <div style="margin-bottom:1.25rem;">
            <label style="display:block; font-size:0.8rem; text-transform:uppercase; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem;">Query Volume: <strong id="benchQueryVal" style="color:var(--accent-cyan);">200 Queries</strong></label>
            <input type="range" id="benchQuerySlider" min="50" max="1000" step="50" value="200" style="width:100%;" oninput="document.getElementById('benchQueryVal').textContent = this.value + ' Queries';" />
          </div>

          <div style="margin-bottom:1.25rem;">
            <label style="display:block; font-size:0.8rem; text-transform:uppercase; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem;">Concurrency: <strong id="benchThreadVal" style="color:var(--accent-cyan);">8 Threads</strong></label>
            <input type="range" id="benchThreadSlider" min="1" max="24" step="1" value="8" style="width:100%;" oninput="document.getElementById('benchThreadVal').textContent = this.value + ' Threads';" />
          </div>

          <div style="margin-bottom:1.25rem;">
            <label style="display:block; font-size:0.8rem; text-transform:uppercase; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem;">Workload Profile</label>
            <select id="benchWorkload" class="filter-select" style="width:100%;">
              <option value="mixed">Mixed Financial Workload</option>
              <option value="aml">AML Suspicious Activity Heavy</option>
              <option value="sec">SEC 10-K Inquiries</option>
              <option value="swift">SWIFT Wholesale Transfers</option>
            </select>
          </div>

          <div style="margin-bottom:1.5rem;">
            <label style="display:block; font-size:0.8rem; text-transform:uppercase; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem;">Custom Query Pool (Optional)</label>
            <textarea id="benchCustomPool" class="input-text" style="width:100%; height:80px; font-family:var(--font-mono); font-size:0.75rem; resize:vertical;" placeholder="Add custom queries, 1 per line..."></textarea>
          </div>

          <button id="btnRunBench" class="btn-action btn-success" style="width:100%; justify-content:center; padding:0.85rem;" onclick="runStressBenchmark()">
            🚀 Execute Stress Test
          </button>
        </div>

        <div class="panel-card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h3 style="font-size:1.1rem; color:#fff;">Live Telemetry & Latency Percentiles</h3>
            <span id="benchStatusBadge" style="font-size:0.8rem; color:var(--text-muted);">Idle — Ready.</span>
          </div>

          <div class="stats-kpi-grid">
            <div class="kpi-tile"><div class="kpi-tile-label">Throughput (QPS)</div><div id="kpiQps" class="kpi-tile-val">--</div></div>
            <div class="kpi-tile"><div class="kpi-tile-label">Median (p50)</div><div id="kpiP50" class="kpi-tile-val">--</div></div>
            <div class="kpi-tile"><div class="kpi-tile-label">p95 Latency</div><div id="kpiP95" class="kpi-tile-val">--</div></div>
            <div class="kpi-tile"><div class="kpi-tile-label">p99 Latency</div><div id="kpiP99" class="kpi-tile-val">--</div></div>
            <div class="kpi-tile"><div class="kpi-tile-label">Process Memory</div><div id="kpiRss" class="kpi-tile-val">--</div></div>
          </div>

          <!-- Interactive Latency Histogram -->
          <div style="background:rgba(0,0,0,0.3); border:1px solid var(--border-color); border-radius:10px; padding:1rem; margin-bottom:1rem;">
            <div style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700; margin-bottom:0.75rem;">Latency Distribution Histogram</div>
            <div id="histogramContainer" style="display:flex; align-items:flex-end; gap:1.25rem; height:90px; padding:0 0.5rem;">
              <div style="color:var(--text-muted); font-size:0.8rem; margin:auto;">Execute stress test to visualize latency buckets.</div>
            </div>
          </div>

          <div class="terminal-window">
            <div class="terminal-header">
              <span>● Stress Execution Output Log</span>
            </div>
            <div id="benchLogTerminal" class="terminal-body" style="min-height:100px; max-height:150px;">Click 'Execute Stress Test' to begin multi-threaded query workload against the 50,000 document segment.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 5: LIVE INGESTION SANDBOX -->
    <section id="ingestTab" class="tab-content">
      <div class="panel-card">
        <h2 style="font-size:1.25rem; margin-bottom:0.4rem;">📝 Real-Time Document Ingestion Playground</h2>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1.5rem;">Test ad-hoc document indexing directly from the UI. The document will be tokenized and inserted into the active memory-mapped index for immediate retrieval without restarting or rebuilding the segment.</p>

        <!-- Quick Fill Templates -->
        <div style="margin-bottom:1.25rem;">
          <span class="chips-label">Quick Fill Templates:</span>
          <button class="chip-btn" onclick="fillIngestTemplate('aml')">AML Structuring Alert</button>
          <button class="chip-btn" onclick="fillIngestTemplate('sec')">SEC Derivatives Disclosure</button>
          <button class="chip-btn" onclick="fillIngestTemplate('swift')">Sanctioned SWIFT Wire</button>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.25rem; margin-bottom:1.25rem;">
          <div>
            <label style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700;">Document Title</label>
            <input type="text" id="ingestTitle" class="input-text" style="width:100%; margin-top:0.35rem;" value="SAR Alert: Layered Off-Ramp Wire Structuring (JPM - US)" />
          </div>

          <div>
            <label style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700;">Regulatory Archetype</label>
            <select id="ingestDocType" class="filter-select" style="width:100%; margin-top:0.35rem;">
              <option value="AML_SAR">AML_SAR (Suspicious Activity Report)</option>
              <option value="SEC_FILING">SEC_FILING (10-K / 10-Q Disclosure)</option>
              <option value="SWIFT_TX">SWIFT_TX (Interbank Wire MT103)</option>
              <option value="CREDIT_UNDERWRITING">CREDIT_UNDERWRITING (Loan Assessment)</option>
            </select>
          </div>

          <div>
            <label style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700;">Institution / Ticker</label>
            <select id="ingestTicker" class="filter-select" style="width:100%; margin-top:0.35rem;">
              <option value="JPM">JPMorgan Chase (JPM)</option>
              <option value="GS">Goldman Sachs (GS)</option>
              <option value="MS">Morgan Stanley (MS)</option>
              <option value="BAC">Bank of America (BAC)</option>
              <option value="C">Citigroup (C)</option>
            </select>
          </div>

          <div>
            <label style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700;">Risk Severity</label>
            <select id="ingestRisk" class="filter-select" style="width:100%; margin-top:0.35rem;">
              <option value="CRITICAL">CRITICAL</option>
              <option value="HIGH">HIGH</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="LOW">LOW</option>
            </select>
          </div>

          <div>
            <label style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700;">Transaction Amount ($ USD)</label>
            <input type="number" id="ingestAmount" class="input-text" style="width:100%; margin-top:0.35rem;" value="3450000" />
          </div>

          <div>
            <label style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700;">Jurisdiction</label>
            <select id="ingestJurisdiction" class="filter-select" style="width:100%; margin-top:0.35rem;">
              <option value="US">US (United States)</option>
              <option value="EU">EU (European Union)</option>
              <option value="UK">UK (United Kingdom)</option>
              <option value="SG">SG (Singapore)</option>
            </select>
          </div>
        </div>

        <div style="margin-bottom:1.5rem;">
          <label style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700;">Narrative Snippet</label>
          <textarea id="ingestSnippet" class="input-text" style="width:100%; height:100px; margin-top:0.35rem; font-family:var(--font-mono); font-size:0.82rem;">Transaction monitoring detected rapid sequential wire transfers avoiding CTR thresholds. Complex nested correspondent accounts used for currency structuring.</textarea>
        </div>

        <div style="display:flex; gap:1rem; align-items:center;">
          <button id="btnIngest" class="btn-action btn-success" onclick="submitLiveIngestion()">
            ⚡ Ingest Document into Live Engine
          </button>
          <button id="btnSearchIngested" class="btn-secondary" style="display:none;" onclick="searchIngestedDoc()">
            🔍 Search This Record Now
          </button>
          <span id="ingestMsg" style="font-size:0.85rem; color:var(--text-muted);"></span>
        </div>
      </div>
    </section>

    <!-- TAB 6: LEXICON & SEGMENTS -->
    <section id="inspectTab" class="tab-content">
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.5rem;">
        <div class="panel-card">
          <h3 style="font-size:1.1rem; color:#fff; margin-bottom:1rem;">Active Segment Files (Disk Footprint)</h3>
          <div id="segmentFilesList">Loading disk segment stats...</div>
        </div>

        <div class="panel-card">
          <h3 style="font-size:1.1rem; color:#fff; margin-bottom:1rem;">Lexicon & Postings Explorer</h3>
          <div class="chips-group" style="margin-bottom:0.75rem;">
            <span class="chips-label">Quick Terms:</span>
            <button class="chip-btn" onclick="lookupLexiconTerm('smurfing')">smurfing</button>
            <button class="chip-btn" onclick="lookupLexiconTerm('basel')">basel</button>
            <button class="chip-btn" onclick="lookupLexiconTerm('derivatives')">derivatives</button>
            <button class="chip-btn" onclick="lookupLexiconTerm('swift')">swift</button>
            <button class="chip-btn" onclick="lookupLexiconTerm('mezzanine')">mezzanine</button>
          </div>
          <input 
            type="text" 
            id="lexiconInput" 
            class="search-input" 
            style="width:100%; margin-bottom:1rem;" 
            placeholder="Type any financial token to inspect postings..."
            oninput="lookupLexiconTerm(this.value)"
          />
          <div id="lexiconResultBox" style="background:rgba(0,0,0,0.4); padding:1rem; border-radius:8px; font-family:var(--font-mono); font-size:0.82rem; min-height:120px;">
            Type a term above to view its document frequency (df), binary byte offset, and sample posting tuples.
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- EVIDENCE LOCKER DRAWER -->
  <div id="evidenceDrawer" class="drawer-overlay">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;">
      <h3 style="font-size:1.15rem; color:#fff;">⭐ Evidence Locker</h3>
      <button class="btn-secondary" onclick="toggleEvidenceLocker()">&times; Close</button>
    </div>
    <p style="font-size:0.82rem; color:var(--text-muted); margin-bottom:1rem;">Pinned regulatory records saved for investigation export.</p>
    <div id="lockerItemsList" style="flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:0.75rem;">
      <div class="empty-state">No records pinned yet. Click 'Pin to Locker' on any result card.</div>
    </div>
    <div style="display:flex; gap:0.5rem; margin-top:1rem; padding-top:1rem; border-top:1px solid var(--border-color);">
      <button class="btn-secondary" style="flex:1; justify-content:center;" onclick="exportLockerJson()">Export Locker</button>
      <button class="btn-secondary" style="flex:1; justify-content:center; color:#f87171;" onclick="clearLocker()">Clear</button>
    </div>
  </div>

  <!-- DOCUMENT MODAL -->
  <div id="docModal" class="modal-overlay" onclick="closeDocModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
        <div style="display:flex; gap:0.5rem; align-items:center;">
          <span id="modalRisk" class="risk-badge">HIGH</span>
          <span id="modalType" class="type-badge">AML_SAR</span>
          <span id="modalTicker" class="ticker-chip">JPM</span>
        </div>
        <button class="btn-secondary" onclick="closeDocModal()">&times; Close</button>
      </div>
      <h2 id="modalTitle" style="font-size:1.25rem; color:#fff; margin-bottom:0.75rem;">--</h2>
      <p id="modalSnippet" style="font-size:0.95rem; color:#cbd5e1; line-height:1.6; margin-bottom:1.5rem;">--</p>
      
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.8rem; text-transform:uppercase; color:var(--text-muted); font-weight:700;">Full Raw Record JSON</span>
        <button class="btn-secondary" onclick="copyModalJson()">📋 Copy JSON</button>
      </div>
      <pre id="modalJson" style="background:#050811; border:1px solid var(--border-color); border-radius:8px; padding:1rem; font-family:var(--font-mono); font-size:0.8rem; color:#93c5fd; overflow-x:auto; margin-top:0.5rem;"></pre>
    </div>
  </div>

  <script>
    let searchDebounceTimer = null;
    let currentResults = [];
    let pinnedRecords = [];
    let lastIngestedId = null;

    // Elements
    const queryInput = document.getElementById('queryInput');
    const tickerFilter = document.getElementById('tickerFilter');
    const riskFilter = document.getElementById('riskFilter');
    const docTypeFilter = document.getElementById('docTypeFilter');
    const jurisdictionFilter = document.getElementById('jurisdictionFilter');
    const limitFilter = document.getElementById('limitFilter');
    const k1Slider = document.getElementById('k1Slider');
    const bSlider = document.getElementById('bSlider');
    const k1Val = document.getElementById('k1Val');
    const bVal = document.getElementById('bVal');
    const explainToggle = document.getElementById('explainToggle');
    const resultsGrid = document.getElementById('resultsGrid');
    const resultsCount = document.getElementById('resultsCount');

    // Navigation
    function switchTab(tabId, el) {
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      document.querySelectorAll('.nav-tab-btn').forEach(b => b.classList.remove('active'));
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');
      if (el) el.classList.add('active');

      if (tabId === 'inspectTab') loadSegmentStats();
    }

    // Live search as you type
    function handleLiveSearch() {
      clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(() => {
        executeSearch();
      }, 180);
    }

    function setBm25Preset(k1, b) {
      k1Slider.value = k1;
      bSlider.value = b;
      k1Val.textContent = k1;
      bVal.textContent = b;
      executeSearch();
    }

    function updateSliders() {
      k1Val.textContent = k1Slider.value;
      bVal.textContent = bSlider.value;
      handleLiveSearch();
    }

    function applyPreset(query, risk, ticker, docType) {
      queryInput.value = query;
      if (risk !== undefined) riskFilter.value = risk;
      if (ticker !== undefined) tickerFilter.value = ticker;
      if (docType !== undefined) docTypeFilter.value = docType;
      executeSearch();
    }

    async function executeSearch() {
      const q = queryInput.value.trim();
      if (!q) return;

      resultsCount.textContent = 'Querying memory-mapped segment...';
      const p = new URLSearchParams({
        q: q,
        k: limitFilter.value,
        mode: 'lexical',
        k1: k1Slider.value,
        b: bSlider.value,
        explain: explainToggle.checked,
      });

      if (tickerFilter.value) p.append('ticker', tickerFilter.value);
      if (riskFilter.value) p.append('risk_level', riskFilter.value);
      if (docTypeFilter.value) p.append('doc_type', docTypeFilter.value);
      if (jurisdictionFilter.value) p.append('jurisdiction', jurisdictionFilter.value);

      try {
        const res = await fetch(`/v1/search?${p.toString()}`);
        if (!res.ok) throw new Error(`Search error: ${res.statusText}`);
        const data = await res.json();
        currentResults = data.results || [];
        renderResultsList(data, resultsGrid);
        renderWaterfall(data.waterfall);
      } catch (err) {
        resultsGrid.innerHTML = `<div class="empty-state" style="color:#ef4444;">Error: ${err.message}</div>`;
        resultsCount.textContent = 'Search failed.';
      }
    }

    function renderWaterfall(wf) {
      if (!wf) return;
      document.getElementById('wfTotalMs').textContent = `${wf.total_ms.toFixed(2)} ms`;
      document.getElementById('wfTokenizeVal').textContent = `${wf.tokenize_ms.toFixed(2)} ms`;
      document.getElementById('wfRetrievalVal').textContent = `${wf.retrieval_ms.toFixed(2)} ms`;
      document.getElementById('wfExplainVal').textContent = `${wf.explain_ms.toFixed(2)} ms`;
      document.getElementById('wfHydrationVal').textContent = `${wf.hydration_ms.toFixed(2)} ms`;

      const tot = Math.max(wf.total_ms, 0.01);
      document.getElementById('wfTokenizeBar').style.width = `${(wf.tokenize_ms / tot * 100).toFixed(1)}%`;
      document.getElementById('wfRetrievalBar').style.width = `${(wf.retrieval_ms / tot * 100).toFixed(1)}%`;
      document.getElementById('wfExplainBar').style.width = `${(wf.explain_ms / tot * 100).toFixed(1)}%`;
      document.getElementById('wfHydrationBar').style.width = `${(wf.hydration_ms / tot * 100).toFixed(1)}%`;
    }

    function renderResultsList(data, container, deltaMap) {
      resultsCount.textContent = `Found ${data.results.length} records (k₁=${data.k1}, b=${data.b}) in ${data.took_ms.toFixed(2)} ms`;

      if (data.results.length === 0) {
        container.innerHTML = '<div class="empty-state">No matching compliance records found for criteria.</div>';
        return;
      }

      const qWords = queryInput.value.toLowerCase().split(/\\s+/).filter(w => w.length > 2);
      const maxScore = Math.max(...data.results.map(r => r.score), 1.0);

      container.innerHTML = data.results.map(item => {
        const risk = item.risk_level || 'HIGH';
        const docType = item.doc_type || 'AML_SAR';
        const ticker = item.ticker || 'JPM';
        const amountStr = item.amount ? `$${Number(item.amount).toLocaleString('en-US', {minimumFractionDigits: 2})}` : '';
        const scorePct = Math.min((item.score / maxScore) * 100, 100);

        let deltaHtml = '';
        if (deltaMap && deltaMap.has(item.doc_id)) {
          const delta = deltaMap.get(item.doc_id);
          if (delta === 'NEW') deltaHtml = '<span class="delta-badge delta-new">NEW IN B</span>';
          else if (delta > 0) deltaHtml = `<span class="delta-badge delta-up">▲ +${delta}</span>`;
          else if (delta < 0) deltaHtml = `<span class="delta-badge delta-down">▼ ${delta}</span>`;
          else deltaHtml = '<span class="delta-badge delta-same">= SAME</span>';
        }

        // Highlight matched terms
        let highlightedSnippet = item.snippet;
        qWords.forEach(w => {
          const reg = new RegExp(`(${w})`, 'gi');
          highlightedSnippet = highlightedSnippet.replace(reg, '<span class="highlight-term">$1</span>');
        });

        let explainHtml = '';
        if (item.explanation && item.explanation.length > 0) {
          explainHtml = `
            <div class="explain-box">
              <span style="font-weight:700; color:var(--accent-cyan);">BM25 Score Contribution</span>
              <table class="explain-table">
                <thead>
                  <tr><th>Term</th><th>tf (Doc)</th><th>df (Corpus)</th><th>IDF</th><th>Contribution</th></tr>
                </thead>
                <tbody>
                  ${item.explanation.map(e => `
                    <tr>
                      <td style="color:var(--accent-cyan); font-weight:700;">${e.term}</td>
                      <td>${e.tf}</td><td>${e.df}</td><td>${e.idf.toFixed(3)}</td>
                      <td style="color:var(--accent-emerald); font-weight:700;">+${e.score_contribution.toFixed(4)}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          `;
        }

        return `
          <div class="result-card">
            <div class="card-meta-top">
              <div class="badges-cluster">
                <span class="risk-badge risk-${risk}">${risk}</span>
                <span class="type-badge">${docType}</span>
                <span class="ticker-chip">${ticker}</span>
                ${deltaHtml}
              </div>
              <div class="score-meter-wrap">
                <div class="score-bar-bg"><div class="score-bar-fill" style="width:${scorePct}%;"></div></div>
                <span style="font-family:var(--font-mono); font-size:0.82rem; color:var(--accent-cyan); font-weight:700;">BM25: ${item.score.toFixed(4)} (#${item.rank})</span>
              </div>
            </div>
            <div class="card-title">${item.title}</div>
            <div class="card-snippet">${highlightedSnippet}</div>
            ${explainHtml}
            <div class="card-meta-bottom">
              <span>ID: <code>${item.doc_id}</code></span>
              ${amountStr ? `<span class="amount-highlight">Volume: ${amountStr}</span>` : ''}
              <div class="card-tools">
                <button class="btn-secondary" onclick="pinRecord('${item.doc_id}')">⭐ Pin</button>
                <button class="btn-secondary" onclick="openDocModal('${item.doc_id}')">🔍 Inspect Record</button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    // A/B Search
    async function executeAbComparison() {
      const qA = document.getElementById('abQueryA').value.trim();
      const qB = document.getElementById('abQueryB').value.trim();
      const gridA = document.getElementById('abResultsA');
      const gridB = document.getElementById('abResultsB');

      gridA.innerHTML = '<div class="empty-state">Running Config A...</div>';
      gridB.innerHTML = '<div class="empty-state">Running Config B...</div>';

      const pA = new URLSearchParams({ q: qA, k: 10, mode: 'lexical', k1: document.getElementById('abSliderK1A').value, b: document.getElementById('abSliderBA').value, explain: false });
      const pB = new URLSearchParams({ q: qB, k: 10, mode: 'lexical', k1: document.getElementById('abSliderK1B').value, b: document.getElementById('abSliderBB').value, explain: false });

      try {
        const [resA, resB] = await Promise.all([
          fetch(`/v1/search?${pA.toString()}`).then(r => r.json()),
          fetch(`/v1/search?${pB.toString()}`).then(r => r.json()),
        ]);

        document.getElementById('abTimeA').textContent = `${resA.took_ms.toFixed(2)} ms`;
        document.getElementById('abTimeB').textContent = `${resB.took_ms.toFixed(2)} ms`;

        const rankMapA = new Map(resA.results.map(r => [r.doc_id, r.rank]));
        const deltaMapB = new Map();

        resB.results.forEach(r => {
          if (rankMapA.has(r.doc_id)) {
            deltaMapB.set(r.doc_id, rankMapA.get(r.doc_id) - r.rank);
          } else {
            deltaMapB.set(r.doc_id, 'NEW');
          }
        });

        renderResultsList(resA, gridA);
        renderResultsList(resB, gridB, deltaMapB);
      } catch (err) {
        gridA.innerHTML = `<div class="empty-state" style="color:#ef4444;">${err.message}</div>`;
        gridB.innerHTML = `<div class="empty-state" style="color:#ef4444;">${err.message}</div>`;
      }
    }

    // Automated Test Suite Runner
    async function runFullTestSuite() {
      const btn = document.getElementById('btnRunSuite');
      const terminal = document.getElementById('testLogTerminal');
      const progressWrap = document.getElementById('testProgressWrap');
      const progressBar = document.getElementById('testProgressBar');

      btn.disabled = true;
      btn.textContent = '⏳ Executing Harness...';
      progressWrap.style.display = 'block';
      progressBar.style.width = '20%';

      terminal.textContent = `[*] Initializing BFSI Sentinel Automated Test Harness...
[*] Verifying on-disk segment checksums and loading worker threads...
`;

      const pills = ['TC01', 'TC02', 'TC03', 'TC04', 'TC05', 'TC06'];
      pills.forEach(p => {
        document.getElementById(`status${p}`).textContent = 'RUNNING';
        document.getElementById(`status${p}`).className = 'test-status-pill status-RUNNING';
      });

      try {
        progressBar.style.width = '60%';
        const res = await fetch('/v1/test/run-suite', { method: 'POST' });
        if (!res.ok) throw new Error(`Test suite error: ${res.statusText}`);
        const data = await res.json();
        progressBar.style.width = '100%';

        let logOut = `[+] Test Suite Completed in ${data.duration_ms} ms
=============================================================
  Total Test Cases:    ${data.total_tests}
  Passed:              ${data.passed_tests}
  Failed:              ${data.failed_tests}
  System Health:       ${data.all_passed ? '100% VERIFIED & PRODUCTION READY' : 'ISSUES DETECTED'}
=============================================================

`;

        data.results.forEach(tc => {
          const id = tc.test_id.replace('-', '');
          const pill = document.getElementById(`status${id}`);
          const sumEl = document.getElementById(`sum${id}`);
          const logEl = document.getElementById(`log${id}`);

          if (pill) {
            pill.textContent = tc.status;
            pill.className = `test-status-pill status-${tc.status}`;
          }
          if (sumEl) sumEl.textContent = `${tc.summary} (${tc.duration_ms} ms)`;
          if (logEl) logEl.textContent = tc.log;

          logOut += `[${tc.status}] ${tc.test_id}: ${tc.name} (${tc.duration_ms} ms)
    -> ${tc.summary}

`;
        });

        terminal.textContent = logOut;
      } catch (err) {
        terminal.textContent = `[ERROR] Failed to run test suite: ${err.message}`;
      } finally {
        btn.disabled = false;
        btn.textContent = '🚀 Run Full Test Suite';
      }
    }

    function toggleTestLog(id) {
      const el = document.getElementById(id);
      el.style.display = el.style.display === 'block' ? 'none' : 'block';
    }

    // Stress Benchmark
    async function runStressBenchmark() {
      const btn = document.getElementById('btnRunBench');
      const badge = document.getElementById('benchStatusBadge');
      const terminal = document.getElementById('benchLogTerminal');

      btn.disabled = true;
      btn.textContent = 'Executing...';
      badge.textContent = 'Running load...';
      terminal.textContent = `Initiating concurrent load generator...
Spawning worker pool against memory-mapped segment...`;

      const customRaw = document.getElementById('benchCustomPool').value.trim();
      const customQueries = customRaw ? customRaw.split('\\n').map(s => s.trim()).filter(s => s.length > 0) : null;

      const payload = {
        query_count: parseInt(document.getElementById('benchQuerySlider').value),
        concurrency: parseInt(document.getElementById('benchThreadSlider').value),
        workload: document.getElementById('benchWorkload').value,
        custom_queries: customQueries
      };

      try {
        const res = await fetch('/v1/benchmark/run', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error(`Stress test failed: ${res.statusText}`);
        const data = await res.json();

        document.getElementById('kpiQps').textContent = `${data.qps}`;
        document.getElementById('kpiP50').textContent = `${data.p50_ms} ms`;
        document.getElementById('kpiP95').textContent = `${data.p95_ms} ms`;
        document.getElementById('kpiP99').textContent = `${data.p99_ms} ms`;
        document.getElementById('kpiRss').textContent = `${data.rss_mb} MB`;

        terminal.textContent = [
          `[+] Benchmark Completed in ${data.duration_seconds}s`,
          `=============================================================`,
          `  Total Queries Executed:   ${data.total_queries} queries`,
          `  Worker Concurrency:       ${data.concurrency} concurrent threads`,
          `  Throughput Achieved:      ${data.qps} QPS`,
          `  Latency min / p50 / max:  ${data.min_ms}ms / ${data.p50_ms}ms / ${data.max_ms}ms`,
          `  Error Count:              ${data.error_count} (0.00% error rate)`,
          `  Process Memory (RSS):     ${data.rss_mb} MB`,
          `=============================================================`
        ].join('\\n');

        // Latency Histogram SVG
        if (data.latency_buckets && data.latency_buckets.length > 0) {
          const maxCount = Math.max(...data.latency_buckets.map(b => b.count), 1);
          const histContainer = document.getElementById('histogramContainer');
          histContainer.innerHTML = data.latency_buckets.map(b => {
            const h = Math.max((b.count / maxCount) * 75, 4);
            return `
              <div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:0.25rem;">
                <span style="font-size:0.7rem; font-family:var(--font-mono); color:var(--accent-cyan); font-weight:700;">${b.count}</span>
                <div style="width:100%; height:${h}px; background:linear-gradient(180deg, var(--accent-cyan) 0%, rgba(2, 132, 199, 0.4) 100%); border-radius:3px 3px 0 0;"></div>
                <span style="font-size:0.65rem; color:var(--text-muted); font-family:var(--font-mono); white-space:nowrap;">${b.bucket}</span>
              </div>
            `;
          }).join('');
        }

        badge.textContent = 'Completed (0% Errors)';
      } catch (err) {
        terminal.textContent = `Error: ${err.message}`;
        badge.textContent = 'Failed';
      } finally {
        btn.disabled = false;
        btn.textContent = '🚀 Execute Stress Test';
      }
    }

    // Dynamic Ingestion
    function fillIngestTemplate(type) {
      if (type === 'aml') {
        document.getElementById('ingestTitle').value = 'AML Alert: Multi-Hop Layered Smurfing Wire (GS - US)';
        document.getElementById('ingestDocType').value = 'AML_SAR';
        document.getElementById('ingestTicker').value = 'GS';
        document.getElementById('ingestRisk').value = 'CRITICAL';
        document.getElementById('ingestAmount').value = '4200000';
        document.getElementById('ingestSnippet').value = 'Compliance monitoring detected rapid structured cash transactions avoiding reporting thresholds with offshore layering.';
      } else if (type === 'sec') {
        document.getElementById('ingestTitle').value = 'SEC 10-Q Disclosure: Off-Balance Sheet Credit Default Swaps (JPM - US)';
        document.getElementById('ingestDocType').value = 'SEC_FILING';
        document.getElementById('ingestTicker').value = 'JPM';
        document.getElementById('ingestRisk').value = 'HIGH';
        document.getElementById('ingestAmount').value = '85000000';
        document.getElementById('ingestSnippet').value = 'Item 7. Quantitative Disclosures. Gross notional derivative contracts and credit default swap exposure increased with central counterparty margining.';
      } else if (type === 'swift') {
        document.getElementById('ingestTitle').value = 'SWIFT MT103 Sanctioned Correspondent Bank Transfer (DB - EU)';
        document.getElementById('ingestDocType').value = 'SWIFT_TX';
        document.getElementById('ingestTicker').value = 'DB';
        document.getElementById('ingestRisk').value = 'CRITICAL';
        document.getElementById('ingestAmount').value = '1750000';
        document.getElementById('ingestSnippet').value = 'SWIFT interbank wire flagged by OFAC SDN screening filter during wholesale FX settlement.';
      }
    }

    async function submitLiveIngestion() {
      const btn = document.getElementById('btnIngest');
      const msg = document.getElementById('ingestMsg');
      const searchBtn = document.getElementById('btnSearchIngested');

      btn.disabled = true;
      btn.textContent = 'Indexing...';
      msg.textContent = 'Tokenizing and inserting in memory...';

      const payload = {
        title: document.getElementById('ingestTitle').value.trim(),
        snippet: document.getElementById('ingestSnippet').value.trim(),
        doc_type: document.getElementById('ingestDocType').value,
        ticker: document.getElementById('ingestTicker').value,
        risk_level: document.getElementById('ingestRisk').value,
        amount: parseFloat(document.getElementById('ingestAmount').value) || null,
        jurisdiction: document.getElementById('ingestJurisdiction').value,
      };

      try {
        const res = await fetch('/v1/ingest/document', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        if (!res.ok) throw new Error(`Ingest failed: ${res.statusText}`);
        const data = await res.json();
        lastIngestedId = data.doc_id;

        document.getElementById('headerDocs').textContent = `${data.corpus_size_now.toLocaleString()} Records`;
        msg.innerHTML = `<strong style="color:var(--accent-emerald);">✓ Ingested ${data.doc_id} in ${data.duration_ms} ms (${data.tokens_indexed} tokens). Available for zero-copy search!</strong>`;
        searchBtn.style.display = 'inline-block';
      } catch (err) {
        msg.innerHTML = `<span style="color:var(--accent-crimson);">${err.message}</span>`;
      } finally {
        btn.disabled = false;
        btn.textContent = '⚡ Ingest Document into Live Engine';
      }
    }

    function searchIngestedDoc() {
      if (lastIngestedId) {
        switchTab('searchTab', document.querySelectorAll('.nav-tab-btn')[0]);
        queryInput.value = document.getElementById('ingestTitle').value;
        tickerFilter.value = document.getElementById('ingestTicker').value;
        riskFilter.value = document.getElementById('ingestRisk').value;
        executeSearch();
      }
    }

    // Segment & Lexicon Explorer
    async function loadSegmentStats() {
      try {
        const res = await fetch('/v1/inspect/stats');
        const data = await res.json();

        const html = data.files.map(f => `
          <div style="display:flex; justify-content:space-between; padding:0.6rem 0; border-bottom:1px solid rgba(255,255,255,0.06); font-family:var(--font-mono); font-size:0.85rem;">
            <span><strong>${f.name}</strong></span>
            <span style="color:var(--accent-cyan);">${f.size_mb} MB (${f.size_bytes.toLocaleString()} bytes)</span>
          </div>
        `).join('');

        document.getElementById('segmentFilesList').innerHTML = html || '<div class="empty-state">No segment files.</div>';
      } catch (err) {
        document.getElementById('segmentFilesList').innerHTML = `<div class="empty-state" style="color:#ef4444;">${err.message}</div>`;
      }
    }

    async function lookupLexiconTerm(val) {
      const term = val.trim().toLowerCase();
      const resBox = document.getElementById('lexiconResultBox');
      document.getElementById('lexiconInput').value = term;
      if (!term) {
        resBox.innerHTML = 'Type a term to inspect its lexicon entry.';
        return;
      }

      try {
        const res = await fetch(`/v1/inspect/term?term=${encodeURIComponent(term)}`);
        const data = await res.json();

        if (data.in_lexicon) {
          const entry = data.lexicon_entry;
          let postingsHtml = '';
          if (data.sample_postings && data.sample_postings.length > 0) {
            postingsHtml = `
              <div style="margin-top:0.75rem; border-top:1px dashed rgba(255,255,255,0.1); padding-top:0.5rem;">
                <div style="color:var(--text-muted); font-size:0.75rem; text-transform:uppercase; margin-bottom:0.25rem;">Sample Postings Tuples (doc_id, tf):</div>
                <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                  ${data.sample_postings.map(p => `
                    <span style="background:rgba(255,255,255,0.06); padding:0.15rem 0.45rem; border-radius:4px; font-size:0.75rem;">
                      ${p.doc_id} <strong style="color:var(--accent-emerald);">(tf:${p.term_frequency})</strong>
                    </span>
                  `).join('')}
                </div>
              </div>
            `;
          }

          resBox.innerHTML = `
            <div>Term: <strong style="color:var(--accent-cyan);">${data.term}</strong></div>
            <div>Document Frequency (df): <strong style="color:var(--accent-gold);">${data.document_frequency.toLocaleString()} documents</strong></div>
            <div>Binary Offset: <code>${entry.offset ? entry.offset.toLocaleString() + ' bytes' : 'Dynamic memory'}</code></div>
            <div>Compressed Length: <code>${entry.length ? entry.length.toLocaleString() + ' bytes' : 'In-memory'}</code></div>
            <div style="margin-top:0.25rem; color:var(--accent-emerald);">Status: Active in Lexicon</div>
            ${postingsHtml}
          `;
        } else {
          resBox.innerHTML = `<span style="color:var(--text-muted);">Term "<strong>${term}</strong>" was not found in active lexicon.</span>`;
        }
      } catch (err) {
        resBox.textContent = `Error: ${err.message}`;
      }
    }

    // Modal Inspection
    let currentModalDoc = null;
    async function openDocModal(docId) {
      const modal = document.getElementById('docModal');
      modal.classList.add('active');

      document.getElementById('modalTitle').textContent = 'Loading record...';
      document.getElementById('modalSnippet').textContent = '';
      document.getElementById('modalJson').textContent = 'Fetching from memory-mapped index...';

      try {
        const res = await fetch(`/v1/document/${docId}`);
        if (!res.ok) throw new Error(`Not found: ${res.statusText}`);
        const data = await res.json();
        currentModalDoc = data;

        document.getElementById('modalTitle').textContent = data.title;
        document.getElementById('modalSnippet').textContent = data.snippet;
        const meta = data.metadata || {};
        const risk = meta.risk_level || 'HIGH';
        const riskEl = document.getElementById('modalRisk');
        riskEl.textContent = risk;
        riskEl.className = `risk-badge risk-${risk}`;

        document.getElementById('modalType').textContent = meta.doc_type || 'AML_SAR';
        document.getElementById('modalTicker').textContent = meta.ticker || 'JPM';
        document.getElementById('modalJson').textContent = JSON.stringify(data, null, 2);
      } catch (err) {
        document.getElementById('modalTitle').textContent = 'Failed to load record';
        document.getElementById('modalSnippet').textContent = err.message;
      }
    }

    function closeDocModal() {
      document.getElementById('docModal').classList.remove('active');
    }

    function copyModalJson() {
      if (currentModalDoc) {
        navigator.clipboard.writeText(JSON.stringify(currentModalDoc, null, 2));
        alert('Record JSON copied to clipboard!');
      }
    }

    // Evidence Locker Drawer
    function toggleEvidenceLocker() {
      const d = document.getElementById('evidenceDrawer');
      d.classList.toggle('active');
    }

    function pinRecord(docId) {
      const doc = currentResults.find(r => r.doc_id === docId);
      if (!doc) return;
      if (!pinnedRecords.find(p => p.doc_id === docId)) {
        pinnedRecords.push(doc);
      }
      renderLocker();
      toggleEvidenceLocker();
    }

    function renderLocker() {
      document.getElementById('lockerCount').textContent = pinnedRecords.length;
      const list = document.getElementById('lockerItemsList');
      if (pinnedRecords.length === 0) {
        list.innerHTML = '<div class="empty-state">No records pinned yet.</div>';
        return;
      }
      list.innerHTML = pinnedRecords.map(item => `
        <div style="background:rgba(0,0,0,0.3); border:1px solid var(--border-color); border-radius:8px; padding:0.75rem;">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
            <span class="risk-badge risk-${item.risk_level || 'HIGH'}">${item.risk_level || 'HIGH'}</span>
            <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--accent-cyan);">${item.doc_id}</span>
          </div>
          <div style="font-size:0.85rem; font-weight:600; color:#fff; margin-bottom:0.25rem;">${item.title}</div>
          <button class="btn-secondary" style="font-size:0.7rem; padding:0.2rem 0.5rem;" onclick="unpinRecord('${item.doc_id}')">Remove</button>
        </div>
      `).join('');
    }

    function unpinRecord(docId) {
      pinnedRecords = pinnedRecords.filter(p => p.doc_id !== docId);
      renderLocker();
    }

    function clearLocker() {
      pinnedRecords = [];
      renderLocker();
    }

    function exportLockerJson() {
      const blob = new Blob([JSON.stringify(pinnedRecords, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `bfsi_evidence_locker_${Date.now()}.json`;
      a.click();
    }

    function exportResultsJson() {
      const blob = new Blob([JSON.stringify(currentResults, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `bfsi_search_results_${Date.now()}.json`;
      a.click();
    }

    function exportResultsCsv() {
      if (!currentResults.length) return alert('No results to export');
      const headers = ['doc_id', 'title', 'ticker', 'risk_level', 'doc_type', 'score', 'rank'];
      const rows = currentResults.map(r => [
        `"${r.doc_id}"`,
        `"${(r.title || '').replace(/"/g, '""')}"`,
        `"${r.ticker || ''}"`,
        `"${r.risk_level || ''}"`,
        `"${r.doc_type || ''}"`,
        r.score,
        r.rank
      ].join(','));
      const csv = [headers.join(','), ...rows].join('\\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `bfsi_search_results_${Date.now()}.csv`;
      a.click();
    }

    // Initial search
    executeSearch();
  </script>
</body>
</html>
"""
