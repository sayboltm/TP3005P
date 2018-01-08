# TP3005P

This is software now just based on a library of sorts copied verbatim from the works of Richard A. Zwicky, Jr. (not
me) on this blog:
http://www.circumflex.systems/2017/06/controlling-tekpower-tp3005p-power.html

This now only makes up TP3005P.py, but this is even getting further dev.

----------------

I purchased one of these just because it had this nice open-source starting
point, but for open source software to grow and spread, it needs the visibility
and ease of collaboration that comes only with version control software such
as Git/Github/Bitbucket etc. 

I cannot make my repos private to work on this, so it is public. But it does
not make sense for me to work on this without it being contained in a git repo.

-----------------------------------------------------
Dependencies:

Use:
Run main.py
See *_example.ini* in ./Config for how to set up the ini files
Note: MUST use consistent naming for a battery configuration. i.e. [Li-Ion] must be spelled the same in c_rates.ini, params.ini AND SOC_OCV.ini!

TODOs:
- Fix remote disconnect requiring power cycle to control from front panel
