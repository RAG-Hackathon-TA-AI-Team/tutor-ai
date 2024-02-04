from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from app.tools.openai.prompt import chunk_time_stamp_prompt
import os



class GPTSummarizer(object):

    def __init__(self):
        self.chunk_prompt = PromptTemplate(
            input_variables=["input"],
            template=chunkize_prompt["instruction"],
        )

        self.chunk_timestamp_prompt = PromptTemplate(
            input_variables=["input"],
            template=chunk_time_stamp_prompt["instruction"],
        )

        self.summary_prompt = PromptTemplate(
            input_variables=["input"],
            template=summarization_prompt["instruction"],
        )
        # gpt 4 model
        # self.llm = ChatOpenAI(temperature=0.1, model="gpt-4")
        # gpt 3 model
        self.llm = ChatOpenAI(temperature=0.1, model= "gpt-4-0125-preview")

    async def chunkize(self, transcriptions) -> Dict[str, Any]:
        # abtain the history turn in Dialogstate
        chain = LLMChain(llm=self.llm, prompt=self.chunk_prompt, verbose=False)
        # combine history prompt with user current term input
        result = chain.predict(input=transcriptions)

        # TODO here that we will also need to log userID later (after we add userID )?
        try:
            # verify format here, make the the format is acceptable
            return result
        except Exception:
            return {}
        

    async def chunkize_timestamp(self, transcription: str):
        # abtain the history turn in Dialogstate
        chain = LLMChain(llm=self.llm, prompt=self.chunk_timestamp_prompt, verbose=False)
        # combine history prompt with user current term input
        result = chain.predict(input=transcription)
        # TODO here that we will also need to log userID later (after we add userID )?
        try:
            # verify format here, make the the format is acceptable
            return result
        except Exception:
            return {}
    