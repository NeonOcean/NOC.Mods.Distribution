import typing

def Format (template: str, **kwargs) -> str:
	return FormatDictionary(template, kwargs)

def FormatDictionary (template: str, formattingDictionary: typing.Dict[str, str]) -> str:
	formattedTemplate = template  # type: str

	for formattingKey, formattingString in formattingDictionary.items():  # type: str, str
		formattingKeyIdentifier = "{<-" + formattingKey + "->}"  # type: str
		formattingKeyIdentifierLength = len(formattingKeyIdentifier)  # type: int

		formattingIndexes = _GetAllIndexes(formattedTemplate, "{<-" + formattingKey + "->}")  # type: typing.List[int]

		while len(formattingIndexes) != 0:
			currentFormattingIndex = formattingIndexes[0]  # type: int
			formattingIndexes.pop(0)

			formattingIndentation = _PreviousWhitespaces(formattedTemplate, currentFormattingIndex)  # type: str
			formattingStringIndented = formattingString.replace("\n", "\n" + formattingIndentation)  # type: str
			formattingStringIndentedLength = len(formattingStringIndented)  # type: int

			formattedTemplate = formattedTemplate[: currentFormattingIndex] + formattingStringIndented + formattedTemplate[currentFormattingIndex + formattingKeyIdentifierLength: ]

			formattingIndexesLength = len(formattingIndexes)  # type: int
			formattingIndexIndex = 0  # type: int

			while formattingIndexIndex < formattingIndexesLength:
				if formattingIndexes[formattingIndexIndex] > currentFormattingIndex:
					formattingIndexes[formattingIndexIndex] += formattingStringIndentedLength - formattingKeyIdentifierLength

				formattingIndexIndex += 1

	return formattedTemplate

def _GetAllIndexes (targetString: str, subString: str) -> typing.List[int]:
	targetStringLength = len(targetString)
	subStringLength = len(subString)  # type: int

	matchingIndexes = list()  # type: typing.List[int]

	if targetStringLength <= 0 or subStringLength <= 0:
		return matchingIndexes

	subStringIndex = 0  # type: int

	targetStringIndex = 0  # type: int
	while targetStringIndex < targetStringLength:
		if targetString[targetStringIndex] == subString[subStringIndex]:

			if subStringIndex == subStringLength - 1:
				matchingIndexes.append(targetStringIndex - subStringIndex)
				subStringIndex = 0
			else:
				subStringIndex += 1
		else:
			subStringIndex = 0

		targetStringIndex += 1

	return matchingIndexes

def _PreviousWhitespaces (text: str, position: int) -> str:
	position -= 1  # type: int
	whitespaces = ""  # type: str

	while position > -1 and not (text[position] == "\n" or text[position] == "\r"):
		if text[position] != "\t" and text[position] != " ":
			whitespaces = ""
		else:
			whitespaces += text[position]

		position -= 1

	return whitespaces