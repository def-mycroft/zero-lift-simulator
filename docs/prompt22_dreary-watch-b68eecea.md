# prompt22  add prompt section to docs dreary-watch b68eecea

#prompt 

random codename: dreary-watch b68eecea

***

when I run `zls dev --build-docs` I get:

```bash-output
Running Sphinx v8.2.3
loading translations [en]... done
making output directory... done
myst v4.0.1: MdParserConfig(commonmark_only=False, gfm_only=False, enable_extensions=set(), disable_syntax=[], all_links_external=False, links_external_new_tab=False, url_schemes=('http', 'https', 'mailto', 'ftp'), ref_domains=None, fence_as_directive=set(), number_code_blocks=[], title_to_header=False, heading_anchors=0, heading_slug_func=None, html_meta={}, footnote_sort=True, footnote_transition=True, words_per_minute=200, substitutions={}, linkify_fuzzy_links=True, dmath_allow_labels=True, dmath_allow_space=True, dmath_allow_digits=True, dmath_double_inline=False, update_mathjax=True, mathjax_classes='tex2jax_process|mathjax_process|math|output_area', enable_checkboxes=False, suppress_warnings=[], highlight_code_blocks=True)
building [mo]: targets for 0 po files that are out of date
writing output... 
building [html]: targets for 75 source files that are out of date
updating environment: [new config] 75 added, 0 changed, 0 removed
reading sources... [  1%] api/index
reading sources... [  3%] api/modules
reading sources... [  4%] api/zero_liftsim
reading sources... [  5%] index
reading sources... [  7%] wiki/00projectanchor-liftsim-burly-concert-gigantic-analysis-e7cf1ccf
reading sources... [  8%] wiki/CONTENTS
reading sources... [  9%] wiki/README
reading sources... [ 11%] wiki/agent-experience
reading sources... [ 12%] wiki/alpha_sim_usage
reading sources... [ 13%] wiki/archived-project-anchors-ultra-tomorrow-1f27d36c
reading sources... [ 15%] wiki/bugfix_add_deps
reading sources... [ 16%] wiki/bugfix_agent_state_circular_import
reading sources... [ 17%] wiki/bugfix_chair_default
reading sources... [ 19%] wiki/bugfix_git_agreeable
reading sources... [ 20%] wiki/bugfix_logger_filepath_finish
reading sources... [ 21%] wiki/bugfix_response_logger_filepath_finish
reading sources... [ 23%] wiki/bugfix_riders
reading sources... [ 24%] wiki/building_trust_simulation
reading sources... [ 25%] wiki/dev_snippets
reading sources... [ 27%] wiki/for_codex_simmanager_docs
reading sources... [ 28%] wiki/git-tools
reading sources... [ 29%] wiki/high_wait_analysis
reading sources... [ 31%] wiki/law_simulation_book
reading sources... [ 32%] wiki/main_notes_adding_wiki_articles
reading sources... [ 33%] wiki/main_notes_as_a_human_how_to_code_with_codex
reading sources... [ 35%] wiki/main_notes_best_practices_coding_with_codex
reading sources... [ 36%] wiki/main_notes_business_value_research
reading sources... [ 37%] wiki/main_notes_checkpoint_prim_classes
reading sources... [ 39%] wiki/main_notes_codex_must_read_this_rules_for_codex
reading sources... [ 40%] wiki/main_notes_development_ref_for_prompts
reading sources... [ 41%] wiki/main_notes_devplan
reading sources... [ 43%] wiki/main_notes_docstring_style_guide
reading sources... [ 44%] wiki/main_notes_flowchart
reading sources... [ 45%] wiki/main_notes_for_codex_update_toc
reading sources... [ 47%] wiki/main_notes_implementation
reading sources... [ 48%] wiki/main_notes_simulation_manager_tutorial
reading sources... [ 49%] wiki/main_notes_styleguide_wiki_articles
reading sources... [ 51%] wiki/main_notes_wiki_article_creation_for_codex
reading sources... [ 52%] wiki/main_notes_wiki_article_template
reading sources... [ 53%] wiki/partial-kernel-tutorial-infer-agent-states
reading sources... [ 55%] wiki/project_questions_orange
reading sources... [ 56%] wiki/prompt0_dev_init_class
reading sources... [ 57%] wiki/prompt10_multi_lift_sim
reading sources... [ 59%] wiki/prompt11_variable_chairs
reading sources... [ 60%] wiki/prompt12_lonely_camera_125058f3
reading sources... [ 61%] wiki/prompt13_pandas_custom
reading sources... [ 63%] wiki/prompt14_agent_explicit_fail_aggressive_week
reading sources... [ 64%] wiki/prompt16_dapper_leading_f5ed905a
reading sources... [ 65%] wiki/prompt17_enchanting-curve-ff38f89e
reading sources... [ 67%] wiki/prompt18_drab-question-bb832036
reading sources... [ 68%] wiki/prompt19_update _func_name-hanging-silly-001b3e58
reading sources... [ 69%] wiki/prompt1_implement_lift
reading sources... [ 71%] wiki/prompt20_breakable_scratch-689c423e
reading sources... [ 72%] wiki/prompt21_wary-bitter-1b487118
reading sources... [ 73%] wiki/prompt22_dreary-watch-b68eecea
reading sources... [ 75%] wiki/prompt2_event_classes
reading sources... [ 76%] wiki/prompt3_agent_class
reading sources... [ 77%] wiki/prompt4_implement_alpha_sim
reading sources... [ 79%] wiki/prompt5_full_agent_logging
reading sources... [ 80%] wiki/prompt6_agent_logging
reading sources... [ 81%] wiki/prompt7_simulation_datetime
reading sources... [ 83%] wiki/prompt8_time_distribution_enhancement
reading sources... [ 84%] wiki/prompt9_clock_simulation_runtime
reading sources... [ 85%] wiki/prompt_15_prompt-agent-traceback-ritzy-call-7e649afc
reading sources... [ 87%] wiki/purpose-of-simulation-voice-memo-thankful-examination-e38a3737
reading sources... [ 88%] wiki/running_tests
reading sources... [ 89%] wiki/time_tracking_enhancement
reading sources... [ 91%] wiki/unnamed-cowardly-leather-d8f8b337
reading sources... [ 92%] wiki/unnamed-crooked-revenue-67c6c0ef
reading sources... [ 93%] wiki/unnamed-dapper-leading-f5ed905a
reading sources... [ 95%] wiki/unnamed-guttural-place-5c711918
reading sources... [ 96%] wiki/unnamed-hellish-point-7ff2842e
reading sources... [ 97%] wiki/unnamed-lyrical-development-efd3227f
reading sources... [ 99%] wiki/unnamed-steady-exit-e6ebfe98
reading sources... [100%] wiki/updating_dependencies

looking for now-outdated files... none found
pickling environment... done
checking consistency... /home/zero/code-repos/zero-lift-simulator/docs-src/api/zero_liftsim.rst: document is referenced in multiple toctrees: ['api/index', 'api/modules'], selecting: api/modules <- api/zero_liftsim
done
preparing documents... done
copying assets... 
copying static files... 
Writing evaluated template result to /home/zero/code-repos/zero-lift-simulator/docs-site/_static/language_data.js
Writing evaluated template result to /home/zero/code-repos/zero-lift-simulator/docs-site/_static/basic.css
Writing evaluated template result to /home/zero/code-repos/zero-lift-simulator/docs-site/_static/documentation_options.js
copying static files: done
copying extra files... 
copying extra files: done
copying assets: done
writing output... [  1%] api/index
writing output... [  3%] api/modules
writing output... [  4%] api/zero_liftsim
writing output... [  5%] index
writing output... [  7%] wiki/00projectanchor-liftsim-burly-concert-gigantic-analysis-e7cf1ccf
writing output... [  8%] wiki/CONTENTS
writing output... [  9%] wiki/README
writing output... [ 11%] wiki/agent-experience
writing output... [ 12%] wiki/alpha_sim_usage
writing output... [ 13%] wiki/archived-project-anchors-ultra-tomorrow-1f27d36c
writing output... [ 15%] wiki/bugfix_add_deps
writing output... [ 16%] wiki/bugfix_agent_state_circular_import
writing output... [ 17%] wiki/bugfix_chair_default
writing output... [ 19%] wiki/bugfix_git_agreeable
writing output... [ 20%] wiki/bugfix_logger_filepath_finish
writing output... [ 21%] wiki/bugfix_response_logger_filepath_finish
writing output... [ 23%] wiki/bugfix_riders
writing output... [ 24%] wiki/building_trust_simulation
writing output... [ 25%] wiki/dev_snippets
writing output... [ 27%] wiki/for_codex_simmanager_docs
writing output... [ 28%] wiki/git-tools
writing output... [ 29%] wiki/high_wait_analysis
writing output... [ 31%] wiki/law_simulation_book
writing output... [ 32%] wiki/main_notes_adding_wiki_articles
writing output... [ 33%] wiki/main_notes_as_a_human_how_to_code_with_codex
writing output... [ 35%] wiki/main_notes_best_practices_coding_with_codex
writing output... [ 36%] wiki/main_notes_business_value_research
writing output... [ 37%] wiki/main_notes_checkpoint_prim_classes
writing output... [ 39%] wiki/main_notes_codex_must_read_this_rules_for_codex
writing output... [ 40%] wiki/main_notes_development_ref_for_prompts
writing output... [ 41%] wiki/main_notes_devplan
writing output... [ 43%] wiki/main_notes_docstring_style_guide
writing output... [ 44%] wiki/main_notes_flowchart
writing output... [ 45%] wiki/main_notes_for_codex_update_toc
writing output... [ 47%] wiki/main_notes_implementation
writing output... [ 48%] wiki/main_notes_simulation_manager_tutorial
writing output... [ 49%] wiki/main_notes_styleguide_wiki_articles
writing output... [ 51%] wiki/main_notes_wiki_article_creation_for_codex
writing output... [ 52%] wiki/main_notes_wiki_article_template
writing output... [ 53%] wiki/partial-kernel-tutorial-infer-agent-states
writing output... [ 55%] wiki/project_questions_orange
writing output... [ 56%] wiki/prompt0_dev_init_class
writing output... [ 57%] wiki/prompt10_multi_lift_sim
writing output... [ 59%] wiki/prompt11_variable_chairs
writing output... [ 60%] wiki/prompt12_lonely_camera_125058f3
writing output... [ 61%] wiki/prompt13_pandas_custom
writing output... [ 63%] wiki/prompt14_agent_explicit_fail_aggressive_week
writing output... [ 64%] wiki/prompt16_dapper_leading_f5ed905a
writing output... [ 65%] wiki/prompt17_enchanting-curve-ff38f89e
writing output... [ 67%] wiki/prompt18_drab-question-bb832036
writing output... [ 68%] wiki/prompt19_update _func_name-hanging-silly-001b3e58
writing output... [ 69%] wiki/prompt1_implement_lift
writing output... [ 71%] wiki/prompt20_breakable_scratch-689c423e
writing output... [ 72%] wiki/prompt21_wary-bitter-1b487118
writing output... [ 73%] wiki/prompt22_dreary-watch-b68eecea
writing output... [ 75%] wiki/prompt2_event_classes
writing output... [ 76%] wiki/prompt3_agent_class
writing output... [ 77%] wiki/prompt4_implement_alpha_sim
writing output... [ 79%] wiki/prompt5_full_agent_logging
writing output... [ 80%] wiki/prompt6_agent_logging
writing output... [ 81%] wiki/prompt7_simulation_datetime
writing output... [ 83%] wiki/prompt8_time_distribution_enhancement
writing output... [ 84%] wiki/prompt9_clock_simulation_runtime
writing output... [ 85%] wiki/prompt_15_prompt-agent-traceback-ritzy-call-7e649afc
writing output... [ 87%] wiki/purpose-of-simulation-voice-memo-thankful-examination-e38a3737
writing output... [ 88%] wiki/running_tests
writing output... [ 89%] wiki/time_tracking_enhancement
writing output... [ 91%] wiki/unnamed-cowardly-leather-d8f8b337
writing output... [ 92%] wiki/unnamed-crooked-revenue-67c6c0ef
writing output... [ 93%] wiki/unnamed-dapper-leading-f5ed905a
writing output... [ 95%] wiki/unnamed-guttural-place-5c711918
writing output... [ 96%] wiki/unnamed-hellish-point-7ff2842e
writing output... [ 97%] wiki/unnamed-lyrical-development-efd3227f
writing output... [ 99%] wiki/unnamed-steady-exit-e6ebfe98
writing output... [100%] wiki/updating_dependencies

generating indices... genindex py-modindex done
writing additional pages... search done
dumping search index in English (code: en)... done
dumping object inventory... done
build succeeded, 118 warnings.

The HTML pages are in ../../home/zero/code-repos/zero-lift-simulator/docs-site.
```

this is okay, but getting some warning. either fix or suppress these, don't want to see them. 

also, the docs site has left-side menu "API Reference". This is great. Now, add a similar one below which, when expanded, expands into a list where all prompts in dir "docs/" with tag "#prompt" are included. reverse sort this list so that prompt docs w/ larger numbers are on top. this should copy the prompt files from "docs/" (as opposed to replace.). this should be constructed automatically when `zls dev --build-docs` is ran. 

