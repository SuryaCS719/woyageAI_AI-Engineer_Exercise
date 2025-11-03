Here is the extracted text from the PDF, neatly formatted for prompt use with an LLM:

***

**Woyage AI BackEnd Engineer Exercise**

**Exercise 1**

**Task:**  
Build a FastAPI backend that accepts an MP4 video file as input and a start position, separates the audio from the video starting exactly at the given start position through to the end of the video, and stores the audio file as an MP3 with the same file name as the video file name in a bucket on AWS S3.

**Objective:**  
- Implement a POST API following these standards:

  - Request Method: **POST**
  - Request Path: **/video/extract-audio**
  - Request Body: **MP4 data**
  - Response Data:
    ```
    {
      "result": "success",
      "message": "Audio extracted.",
      "data": {
        "audio_path": "aduio_data/FILE_NAME.mp3"
      }
    }
    ```

- You may use any Python framework libraries for parsing.

- Store the extracted data on the AWS S3 Bucket.

**Deliverables:**  
- Professionally written code must be made available on GitHub. (No code by email.)

