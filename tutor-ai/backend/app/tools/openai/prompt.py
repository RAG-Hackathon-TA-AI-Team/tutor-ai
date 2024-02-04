chunk_time_stamp_prompt = {
     "instruction": """You are very good at segmenting text based on the context. Given a video transcript, with timestamp at the end of each sentece, please segment the text into different sections based on the video context. Remember
    to give detailed summarized title to each section. You should segment the text based on the best global context you can get. Make sure there are enough information in each chunk so that the user can understand the context of the chunk.

    Input: a paragraph of text (Ex: Looking at her father’s brutally murdered body[start: 0, end: 12], Oiwa was sick with despair.[start: 12, end: 15] Her father had been Oiwa’s only hope.[s: 16, e: 21] ...
    Output: [
        /
            "title": "Oiwa's father was Oiwa's only hope, but he was brutally murdered",
            "start": 0,
            "end": 21
        /
        ,
        /
            "title": "short detailed sentence summarized title",
            "start": 23,
            "end": 56
        \,
        ...
    ]
    
    Instruction: 
        You are given the timestamp of each sentence, [s:,e:], where s is the start time of the sentence, and e is the end time of the sentence.
        Strictly follow the format of the output.
        The output should be a list of dictionaries.
        Each dictionary should have two keys: "title",  "start", and "end".
        The value of "title" should be a string, a detailed summary of the text with respect to the global context, and should be less than 20 words, the title should be specific and related to video topics. 
        It is okay to skip some sentences if you think they are not important, ONLY include most context related information in each chunk.

    Input: {input}
    Output: 
    """
}
