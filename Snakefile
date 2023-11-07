rule all:
    input:
	    'data/neoantigens.arrow',
		'data/survival.arrow'

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
