#(C) Akimasa 2006

# setup.py
from distutils.core import setup
from glob import glob
import py2exe

py2exe_options = {
	'optimize' : 2,
	'bundle_files' : 1
}

setup(
	name = 'MisileMatador',
	options = {'py2exe' : py2exe_options},
	data_files = [
			('data\\image', glob('data\\image\\*.png')),
			('data\\sound', glob('data\\sound\\*.wav')),
			('data\\field', glob('data\\field\\*.fmf')),
			('', glob('*.txt')),
			('src\\', glob('*.py')),
			('', ["save.dat"]),
			('src\\util', glob('util\\*.py'))
	],
	windows = [
		{
			'script' : 'MissileMatador.py',
			#'icon_resources' : [(1, 'general.ico')]
		}
	]
)
