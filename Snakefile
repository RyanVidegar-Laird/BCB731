rule all:
    input: 'notebooks/overfit.html'

rule render_hw01:
	input:
		neo = 'data/neoantigens.arrow',
		surv = 'data/survival.arrow',
		overfit_nb = 'notebooks/overfit.ipynb'

	output:
		'notebooks/overfit.html'

	shell:
		"""
		quarto render notebooks/overfit.ipynb
		"""

rule preprocess:
	input:
		script = 'src/00-preprocess.py',
		neoraw = 'data/nature24473_MOESM4_neoantigens.xlsx',
		survraw = 'data/nature24473_MOESM5_survival.xlsx'
		
	output:
		neo = 'data/neoantigens.arrow',
		surv = 'data/survival.arrow'	
	shell:
		"""
		{input.script} {input.neoraw} {input.survraw}
        """
