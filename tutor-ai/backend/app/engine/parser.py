from typing import Sequence, Any, List

from app.engine.schema import VideoMetaType
from llama_index.node_parser.interface import NodeParser
from llama_index.node_parser import SentenceSplitter
from llama_index.schema import BaseNode, Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

SYSTEM_MESSAGE = """\
You are an expert in describing a sequence of continuous frames in a video. Given
several frames, provide a alternative text corresponding to the content, action, phenomenon, or
event in the video. 

The resulting text will be used as search index for the video chunk; therefore, it should be
concise and descriptive.
"""


def get_frames_to_text_chain(encoded_frames: List[str]):
    vision_llm = ChatOpenAI(
        model_name="gpt-4-vision-preview"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_MESSAGE),
            MessagesPlaceholder(variable_name="frames")
        ]
    )

    return prompt | vision_llm | StrOutputParser()

def parse_transcript_nodes(docs: List[Document]) -> List[BaseNode]:
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=32)
    return splitter.get_nodes_from_documents(docs)


def parse_keyframe_nodes(docs: List[Document]) -> List[BaseNode]:
    frames_to_text_chain = get_frames_to_text_chain([doc.text for doc in docs])



class VideoNodeParser(NodeParser):
    include_metadata: bool = False
    include_prev_next_rel: bool = False

    def _parse_nodes(
            self,
            nodes: Sequence[Document],
            show_progress: bool = False,
            **kwargs: Any,
    ) -> List[BaseNode]:
        transcript_nodes = [node for node in nodes if node.metadata["type"] == VideoMetaType.TRANSCRIPT]
        keyframe_nodes = [node for node in nodes if node.metadata["type"] == VideoMetaType.KEYFRAME]

        return parse_transcript_nodes(transcript_nodes) + keyframe_nodes
