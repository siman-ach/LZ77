# LZ77 Compression

an Implementation of the LZ77 compression algorithm in Python.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bitarray. 
Open 'Compression.py' and use the listed method below to compress a file. Open 'Decompressor.py' to decompress a file using the guidance given below.

```bash
pip install bitarray
```

## Usage

```python
#calls on the function
compressor = LZ77Alg(window_size=400) #set the window size, it is optional, however higher window size recomended for larger files
```
## Compressing Files

```python
#input the file to compress here
compress_input='/Users/shreya/Desktop/...'
#input the selected output path here
compress_output='/Users/shreya/Desktop/output.txt'
# compress the input file and write it as binary into the output file
compressor.compressor(compress_input, compress_output)
```
Note: If verbose is set to True, then standard output format is printed to the console. It is of a triplet <o , l, c> form, where ‘o’ stands for offset, ‘l’ is length of the match and ‘c’ is the next symbol to be encoded.


## Decompressing Files

```python
#calls on the function
compressor = LZ77Alg(window_size=40) #set the window size, it is optional

#takes the compressed output file to decompress here
compress_output='/Users/shreya/Desktop/output.txt'
#input the selected output path here
output_path = '/Users/shreya/Desktop/decompressed.txt'

# decompress the input file and write it as binary into the output file
compressor.decompressor(compress_output, output_path)
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
```
## Test Files (Examples)
The folder called 'test_files', contains a few test examples: 'othello_eng.txt' which has been compressed to 'output.txt', and has been decompressed back to its original size in 'decompressed.txt'. This file also contains other files which were used during testing (e.g.) Book - Charles Darwin - Natural Selection, can be found in three different languages and tested with the algorithm (charts shown with results in Literature Review)

## License
[MIT](https://choosealicense.com/licenses/mit/)
