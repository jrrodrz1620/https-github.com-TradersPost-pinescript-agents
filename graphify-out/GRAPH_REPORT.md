# Graph Report - .  (2026-06-04)

## Corpus Check
- 414 files · ~130,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 414 nodes · 616 edges · 27 communities (14 shown, 13 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 65 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]

## God Nodes (most connected - your core abstractions)
1. `Pine Script v6 Function Index` - 17 edges
2. `NQ AI BOT App` - 15 edges
3. `App Shell Layout` - 14 edges
4. `Walk-Forward Analyzer App` - 13 edges
5. `pine-developer Skill` - 12 edges
6. `Agent Documentation Map` - 12 edges
7. `Pine Script Development Workflows` - 12 edges
8. `Pine Script v6 Language Reference` - 11 edges
9. `Pine Script v6 Namespaces Reference` - 11 edges
10. `VideoAnalyzer Class` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Static File Middleware` --references--> `NQ AI BOT App`  [INFERRED]
  server.js → index.html
- `PWA Install Prompt Handler` --references--> `NQ AI Bot PWA Manifest`  [INFERRED]
  index.html → manifest.json
- `GET / Route` --references--> `NQ AI BOT App`  [EXTRACTED]
  server.js → index.html
- `NQ AI Trading Bot App Identity` --conceptually_related_to--> `ICT Smart Money Concepts (SMC) Trading Strategy`  [INFERRED]
  manifest.json → index.html
- `Analyze Market PWA Shortcut` --references--> `Analyze Page (AI Signal Form)`  [EXTRACTED]
  manifest.json → index.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Claude Code Hook Lifecycle Pipeline** — hooks_json_hooks_config, hooks_startup_startup_hook, hooks_user_prompt_submit_prompt_hook, hooks_before_write_write_guard, hooks_before_delete_delete_guard, hooks_after_edit_pine_validator, hooks_after_rename_blank_manager [EXTRACTED 1.00]
- **YouTube Video to Pine Script Spec Pipeline** — root_analyze_video_analyze_video, tools_video_analyzer_video_analyzer_class, tools_video_analyzer_get_transcript, tools_video_analyzer_extract_key_concepts, tools_video_analyzer_identify_strategy_components, tools_video_analyzer_generate_pine_script_spec, analysis_video_4c0e6145_analysis_result [EXTRACTED 1.00]
- **File Protection System** — concept_lock_unlock_mechanism, hooks_before_write_write_guard, hooks_before_delete_delete_guard, hooks_user_prompt_submit_prompt_hook, claude_protected_paths_protection_policy [EXTRACTED 1.00]
- **Pine Script Specialized Skill Set** — skills_pine_backtester_skill, skills_pine_debugger_skill, concept_pine_script_agent_routing, hooks_user_prompt_submit_prompt_hook [INFERRED 0.85]
- **All Pine Script Skills** — skills_pine_developer_skill, skills_pine_manager_skill, skills_pine_optimizer_skill, skills_pine_publisher_skill, skills_pine_visualizer_skill [EXTRACTED 1.00]
- **Pine Script v6 Advanced Documentation** — docs_advanced_collections, docs_advanced_libraries, docs_advanced_polylines, docs_advanced_security, docs_advanced_type_casting [EXTRACTED 1.00]
- **New Indicator Development Workflow** — skills_pine_visualizer_skill, skills_pine_developer_skill, skills_pine_optimizer_skill, skills_pine_publisher_skill, skills_pine_manager_skill [EXTRACTED 1.00]
- **Pine Script Core Concepts** — docs_core_execution_model, docs_core_repainting, concept_bar_by_bar_execution, concept_repainting [INFERRED 0.95]
- **PineScript Agents Version History** — concept_version_100, concept_version_120, concept_version_130, root_changelog [EXTRACTED 1.00]
- **Pine Script Debugging Documentation Suite** — debugging_common_errors_doc, debugging_tools_doc, debugging_edge_cases_doc, debugging_performance_doc [EXTRACTED 1.00]
- **Pine Script v6 Function Namespace Documentation** — functions_array_matrix_map_doc, functions_drawing_doc, functions_input_doc, functions_math_doc, functions_request_doc, functions_strategy_doc, functions_technical_doc, functions_timeframe_doc [EXTRACTED 1.00]
- **Pine Script Indicator Development Documentation** — indicators_calculations_doc, indicators_plotting_doc, indicators_structure_doc [EXTRACTED 1.00]
- **Pine Script v6 Quick Reference Suite** — quick_reference_common_patterns_doc, quick_reference_limitations_doc, quick_reference_syntax_basics_doc [EXTRACTED 1.00]
- **Pine Script v6 Core Language Documentation** — language_reference_doc, reference_tables_builtin_variables_doc, quick_reference_syntax_basics_doc [INFERRED 0.95]
- **Strategy Order Management Functions** — functions_strategy_entry, functions_strategy_exit, functions_strategy_close, functions_strategy_close_all, functions_strategy_cancel [EXTRACTED 1.00]
- **Performance and Limitation Concepts** — quick_reference_limitations_security_calls, quick_reference_limitations_visual_elements, quick_reference_limitations_historical_data, debugging_performance_security_calls, debugging_performance_drawing_objects, debugging_performance_historical_buffer [INFERRED 0.85]
- **Drawing Objects Family** — functions_drawing_line, functions_drawing_label, functions_drawing_box, functions_drawing_polyline [EXTRACTED 1.00]
- **Pine Script Data Structures** — functions_array_matrix_map_arrays, functions_array_matrix_map_matrices, functions_array_matrix_map_maps [EXTRACTED 1.00]
- **Technical Analysis Calculation Implementations** — indicators_calculations_sma, indicators_calculations_ema, indicators_calculations_rsi, indicators_calculations_macd, indicators_calculations_bollinger, indicators_calculations_atr, indicators_calculations_vwap [EXTRACTED 1.00]
- **Pine Script v6 Reference Tables Suite** — reference_tables_function_index_doc, reference_tables_keywords_doc, reference_tables_namespaces_doc, reference_tables_operators_doc [INFERRED 0.95]
- **Pine Script Development Agent Team** — concept_pine_manager_agent, concept_pine_developer_agent, concept_pine_visualizer_agent, concept_pine_debugger_agent, concept_pine_backtester_agent, concept_pine_optimizer_agent, concept_pine_publisher_agent [EXTRACTED 1.00]
- **Pine Script Visual Components** — visual_components_plots_doc, visual_components_tables_doc, concept_drawing_functions, concept_plot_functions [INFERRED 0.95]
- **Strategy Development Core Components** — concept_strategy_entry_exit, concept_position_sizing, concept_risk_management, concept_strategy_performance_metrics, concept_backtesting_best_practices [INFERRED 0.95]
- **Video Analysis Python Dependencies** — concept_ytdlp_dependency, concept_youtube_transcript_api, concept_video_analysis_process, concept_pine_visualizer_agent [EXTRACTED 1.00]
- **Pine Script v6 Namespace Suite** — concept_ta_namespace, concept_math_namespace, concept_str_namespace, concept_array_namespace, concept_matrix_namespace, concept_map_namespace, concept_request_namespace, concept_strategy_namespace, concept_input_namespace, concept_color_namespace [EXTRACTED 1.00]
- **Project Scoping and Specification Workflow** — docs_project_scoping_flow_doc, docs_scoping_questions_doc, concept_project_scoping_flow, concept_project_specification, concept_pine_manager_agent [EXTRACTED 1.00]

## Communities (27 total, 13 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (59): AI Trading Analysis Prompt, AllOrigins CORS Proxy, analyze() — Claude AI Signal Function, Anthropic Claude API (claude-sonnet-4-20250514), App Shell Layout, runBacktest() — Simulated Backtest Engine, Backtest Strategies (MultiVWAP, ProTrader, VP+EMA, Combined), Anthropic Claude API (+51 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (40): Adaptive Project Scoping Strategy, Bar-by-Bar Execution Model, Collections (Arrays, Matrices, Maps), Pine Script Feasibility Assessment, File Protection System (lock/unlock), Claude Code Hooks System, Pine Script Line Wrapping Rules, Pine Script Libraries (+32 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (39): Broker Emulator Quirks Edge Case, Data Quality Issues Edge Case, Pine Script Edge Cases and Special Scenarios, First Bar Calculations Edge Case, Illiquid Market Handling Edge Case, Pre/Post Market Data Edge Case, Different Session Types Edge Case, Symbol Changes and Splits Edge Case (+31 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (38): bgcolor() for Visual Debugging, Debug Modes with input.bool(), Pine Script Debugging Tools, label.new() for Debug Information, log.* Functions for Console Output, Performance Profiling Methods, plot() for Value Debugging, table.new() for Debug Dashboards (+30 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (36): Array Operations Namespace (array.*), Backtesting Best Practices, Color Functions Namespace (color.*), Conditional Plotting Techniques, Drawing Functions (line, label, box, polyline), Input Functions Namespace (input.*), Map Operations Namespace (map.*), Mathematical Functions Namespace (math.*) (+28 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (33): Common Pine Script v6 Errors and Solutions, Lookahead and Repainting Error, Cannot Use Mutable Variable Error, NA Value Handling Error, Cannot Use Plot in Local Scope Error, Script Too Large Error, Series vs Simple Context Error, Syntax Error (+25 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (32): math.abs() Function, math Constants (pi, e, phi, rphi), Pine Script v6 Math Functions, math Logarithmic and Exponential Functions, math.min() / math.max() Functions, math.random() Function, math Trigonometric Functions (sin/cos/tan), ta.crossover() / ta.crossunder() Signal Functions (+24 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (25): calc_metrics Function, Contract Value Multiplier (NQ/MNQ/ES/MES), NumPy Dependency, openpyxl Dependency, Pandas Dependency, Plotly Dependency, Streamlit Dependency, equity_curve_fig Function (+17 more)

### Community 8 - "Community 8"
Cohesion: 0.19
Nodes (22): Indicator Development Workflow, Keyword Extraction from Video Transcripts, Multi-Agent Workflow, Pine Backtester Agent, Pine Debugger Agent, Pine Developer Agent, Pine Manager Agent, Pine Optimizer Agent (+14 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (21): Video Analysis Result (video_analysis_4c0e6145.json), Statusline Script (statusline.sh), Pine Script Specification Generation from Video, YouTube Transcript Extraction Pipeline, Analyze Video Shell Wrapper (analyze-video.sh), Package Manifest (package.json), Run Analysis Script (run_analysis.py), analyze Method (main entry) (+13 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (19): Onboarding Documentation, Protected Paths Policy (protected-paths.json), Blank Pine Template Lifecycle Pattern, Lock/Unlock File Protection Mechanism, Onboarding State Management, Pine Script Agent Routing by Keyword, Pine Script Validation Hook Pattern, After Edit Pine Validator (after-edit.sh) (+11 more)

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (17): Alert Functions, Advanced Pine Script Examples (>300 lines), Intermediate Pine Script Examples (100-300 lines), Simple Pine Script Examples (<100 lines), ICT Trading Concepts (Order Blocks, FVG, Liquidity), Multi-Timeframe Analysis, Repainting Prevention Techniques, Smart Money Concepts (SMC) (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.15
Nodes (14): Arithmetic Operators, Assignment Operators (=, :=, +=, etc.), Comparison Operators, Import and Export Library Keywords, Logical Operators (and, or, not), Operator Precedence Rules, Reserved Keywords, Script Type Declarations (indicator, strategy, library) (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.40
Nodes (6): Express Dependency, Trading Dashboard Package, Express Application Server, PORT Environment Config, GET / Route, Static File Middleware

## Knowledge Gaps
- **114 isolated node(s):** `Analyze Video Shell Wrapper (analyze-video.sh)`, `Start Shell Script (start.sh)`, `Package Manifest (package.json)`, `Run Analysis Script (run_analysis.py)`, `TRADING_KEYWORDS Constant` (+109 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Pine Script v6 Language Reference` connect `Community 3` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `Pine Script v6 Namespaces` connect `Community 6` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `Technical Analysis Namespace (ta.*)` connect `Community 4` to `Community 1`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **What connects `Analyze Video Shell Wrapper (analyze-video.sh)`, `Start Shell Script (start.sh)`, `Package Manifest (package.json)` to the rest of the system?**
  _116 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.061952074810052604 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.10384615384615385 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.059379217273954114 - nodes in this community are weakly interconnected._