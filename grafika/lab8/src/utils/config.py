GL_VERSION = (3, 3)
WINDOW_TITLE = 'WMM Lab8'

FRAGMENT_SHADER_EXTENSION = ['.frag']
VERTEX_SHADER_EXTENSION = ['.vert']

def get_supported_extensions():
    return [
        *VERTEX_SHADER_EXTENSION,
        *FRAGMENT_SHADER_EXTENSION
    ]
