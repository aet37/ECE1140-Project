"""Module containing class to implement the emitting phase"""

class Emitter():
    """Class responsible for outputting requests"""
    def __init__(self, full_path):
        self.full_path = full_path
        self.requests = ""

    def emit(self, request):
        """Emits a single request."""
        self.requests += request

    def emit_line(self, request):
        """Emits a single request followed by a newline."""
        self.requests += request + '\n'

    def write_file(self):
        """"Writes the requests to a file."""
        with open(self.full_path, 'w') as output_file:
            output_file.write(self.requests)