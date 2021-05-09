import sys
sys.path
sys.executable
import math
from bitarray import bitarray

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


    def decompressor(self, compress_output, output_path=None): #function for decompressing the given file
        """
            The data is compressed back to its original form, and is output to the given file path.
            If there is no path given, it is returned as a string.
        """

        output_buff = []
        data = bitarray(endian='big')

        #read input file

        try:
            with open(compress_output, 'rb') as input_f:
                data.fromfile(input_f)

        except IOError:
            print ('Error while opening the input file!')

        while len(data) >=9:

            #print("somestring", len(data))
            flag = data.pop(0)

            if not flag:
              byte = data[0:8].tobytes()

              output_buff.append(byte)
              del data[0:8]
            else:
              byte1 = ord(data[0:8].tobytes())
              byte2 = ord(data[8:16].tobytes())

              del data[0:16]
              distance = (byte1 << 4) | (byte2 >> 4)
              length = (byte2 & 0xf)

              for i in range(length):
                  try :
                      output_buff.append(output_buff[-distance])
                  except IndexError:
                      continue

        out_data =  b''.join(output_buff)

        if output_path:

            try:
                with open(output_path, 'wb') as output_f: #writes to the relevant output file
                    output_f.write(out_data)

                    print('Succesfully decompressed the given file!') #if succesfully decompressed prints this string

                    return None

            except IOError:
              print('Cannot write to file path. Please check given file path!') #if unsucessful decompression/ error prints this string
              raise

#calls on the function
compressor = LZ77Alg(window_size=40) #set the window size, it is optional


#takes the compressed output file to decompress here
compress_output='/Users/shreya/Desktop/output.txt'
#input the selected output path here
output_path = '/Users/shreya/Desktop/decompressed.txt'

# decompress the input file and write it as binary into the output file
compressor.decompressor(compress_output, output_path)
