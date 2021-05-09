import sys
sys.path
sys.executable

import math #imports the required math module
from bitarray import bitarray #import bitarray


class LZ77Alg:
    """
    Implementation of the LZ77 Compression Algorithm ('Sliding-Window Compression').

    The compressor maintains a window of size n bytes and a "lookahead buffer" (the contents of which it
    tries to find a match for in the window ).
    When an input file is given, the content of it is compressed by applying this algorithm.
    """

    WINDOW_SIZE_MAX = 400 #the maximum window size

    def __init__(self, window_size=20):  # self constructor method
            self.window_size = min(window_size, self.WINDOW_SIZE_MAX)
            self.size_lookahead_buffer = 15 # the length of the match at most can be 4 bits

    def compressor(self, compress_input, compress_output=None, verbose=False):
        """
        Using the algorithm, the requested input file is compressed.
        The new compressed format will be :
        1 bit followed by 12 bits pointer (it is the distance to the start of the match from the
        present position) and 4 bits (total match length).

        If there are no previous matches found wihtin the window : 0 bit followed by 8 bits (1 byte).

        The then compressed data is written into a binary file (given that the output path is provided).
        If no path is provided, it is returned as a bitarray.

        If 'verbose' is 'True', the compression will print to the console as standard output.
        """

        data = None
        output_buff = bitarray(endian='big')
        i = 0

        try:
            with open(compress_input, 'rb') as input_file:  #read input file
                data = input_file.read()
        except IOError:
            print ('Error while Opening Input File!')
            raise

        while i < len(data):
            #print i

            match = self.findMatch(data, i)

            if match:
                #add 1 bit flag, 12 bit for distance and 4 bit for match length.
                (matchDistance, matchLength) = match

                output_buff.append(True)
                output_buff.frombytes(bytes([matchDistance >> 4]))
                output_buff.frombytes(bytes([((matchDistance & 0xf) << 4) | matchLength]))

                if verbose:
                    print("<1, %i, %i>" % (matchDistance, matchLength))

                i += matchLength

            else :
                #If no match is found, add 0 bit flag, and 8 bit for the character.
                output_buff.append(False)
                output_buff.frombytes(bytes([data[i]]))

                if verbose:
                    print ("<0, %s>" % data[i])

                i += 1

        # if the number of bits is not a multiple of 8, fill buffer with 0s

        output_buff.fill()
        #if a path is given, write the compressed data into binary File
        if compress_output:
            try:
                with open(compress_output, 'wb') as output_file:
                    output_file.write(output_buff.tobytes())
                    print("Successfully compressed file, and saved to given output path!")
                    return None
            except IOError:
                print('Error while trying to write to output file. Please check output file path')
                raise

        #return the compressed data is path is not given.
        return output_buff

    def findMatch(self, data, present_position):

        """
        Function looks for the longest match to a substring.
        It starts at the present position in the lookahead buffer from the window.
        """

        buffer_end = min(present_position + self.size_lookahead_buffer, len(data) +1)

        match_distance = -1
        match_length = -1

        #Only consider substrings with a length of 2 or greater
        #Outputs any substring of length 1
        #for the flag, distance, length

        for j in range(present_position +2, buffer_end):

            start_index = max(0, present_position - self.window_size)
            substring = data[present_position: j]

            for i in range (start_index, present_position):

                repeats = len(substring) // (present_position - i)

                last = len(substring) % (present_position - i)

                string_match = data[i:present_position] * repeats + data[i:i+last]

                if string_match == substring and len(substring) > match_length:
                    match_length = len(substring)
                    match_distance = present_position - i

        if match_distance > 0 and match_length > 0 :
            return ( match_distance, match_length )
        return None


#calls on the function
compressor = LZ77Alg(window_size=400) #set the window size, it is optional, however higher window size recomended for larger files

#input the file to compress here
compress_input='/Users/shreya/Desktop/dblp.xml.00001.1.txt'
#input the selected output path here
compress_output='/Users/shreya/Desktop/output.txt'
# compress the input file and write it as binary into the output file
compressor.compressor(compress_input, compress_output)
