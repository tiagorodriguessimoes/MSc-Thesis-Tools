# MSc-Thesis-Tools

Some tools used for preprocessing text in Portuguese. The default format of the csv files used as input had a category followed by a message, i.e., "C", "some message.".

- csv2arff.py => converts a csv to a arff file.
- removePunct.py => removes punctuation from a given file. You can choose what punctuation to remove.
- removeStopwords.py => removes Portuguese stop-words from texts in a file.
- removeStringsShorterThan.py => removes entries if the message /text is shorten than a given size.
- removeTermsShorterThan.py => removes words / features shorter than a given size.
- replaceNumbers.py => replaces numbers (such as hours, dates, currency) in a airline environment text messages.

extraFunctions.py contains some functions such as HTML parsers, emoji identifier that might be useful for preprocessing text.
