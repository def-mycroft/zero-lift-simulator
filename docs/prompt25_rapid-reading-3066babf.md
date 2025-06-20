# prompt25 Redo seed state again - rapid-reading 3066babf

random codename: rapid-reading 3066babf

#prompt

***
https://chatgpt.com/codex/tasks/task_e_6854b1e162e883238447e0d304facdd4

review the prompt history. see `# TODO - rapid-reading 3066babf` in the cli code, i.e. i've added some sandbox code to --exec-hook. 

so, follow the imports from the cli code and see what code is running. then, review prior prompts and anything else related to setting a simulation seed. then fix this problem and try to write some more tests. focus tests on data points like average weight, beause these are things that need to be fixed for reproducibility. things like agent uuid or something like that aren't impronat to reproducubility, not for practical utility. 

but basiclaly implement a fix so tha it passes the text in sandbox --exec-hook

