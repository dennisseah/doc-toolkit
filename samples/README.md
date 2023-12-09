# Samples

## 1. Summarization of PDF file content

Given a PDF file in blob storage, we do the following

1. Create SAS Token for the pdf file
2. Send the SAS Token to Azure Form Recognizer
3. Parse the Form Recognizer result to extract textual information
4. Write the textual information to blob storage container.
5. Summarize the text with Azure OpenAI

### Instruction

Copy `.env.sample` as .env in the root folder of git, and fill in the values for
the file

to run: `python -m samples.summarization`
