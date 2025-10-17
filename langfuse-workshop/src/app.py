from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse import types as lf_types
from openai import OpenAI
import uuid

# Load environment variables from .env or .env.template
if os.path.exists(".env"):
    load_dotenv(".env")
elif os.path.exists(".env.template"):
    load_dotenv(".env.template")
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse import types as lf_types
from openai import OpenAI

# Load environment variables
if os.path.exists('.env'):
    load_dotenv('.env')
elif os.path.exists('.env.template'):
    load_dotenv('.env.template')

# Initialize clients
lf = Langfuse(
    public_key=os.environ.get('LANGFUSE_PUBLIC_KEY'),
    secret_key=os.environ.get('LANGFUSE_SECRET_KEY'),
    host=os.environ.get('LANGFUSE_HOST', 'https://cloud.langfuse.com')
)

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'message is required'}), 400

    try:
        # Create a trace id and set trace metadata
        trace_id = lf.create_trace_id()
        lf.update_current_trace(name='chat-endpoint', user_id=data.get('user_id', 'anonymous'), metadata={'request_message': data.get('message')})

        # Use a span context manager for the OpenAI call
        trace_context = lf_types.TraceContext(trace_id=trace_id)
        with lf.start_as_current_span(trace_context=trace_context, name='openai-completion') as span:
            resp = client.chat.completions.create(
                model='gpt-4',
                messages=[{'role': 'user', 'content': data['message']}]
            )

            # Try to extract answer (supports multiple OpenAI SDK response shapes)
            answer = None
            try:
                answer = resp.choices[0].message.content
            except Exception:
                if isinstance(resp, dict):
                    choices = resp.get('choices')
                    if choices and isinstance(choices, list) and len(choices) > 0:
                        answer = choices[0].get('message', {}).get('content') or choices[0].get('text')
                if answer is None:
                    answer = str(resp)

            # Update span with output and metadata (end() doesn't take parameters)
            span.update(output=answer, metadata={'model': 'gpt-4', 'response_preview': answer[:200] if answer else None})
            span.end()

        # Score and flush
        lf.score_current_trace(name='response_length', value=len(answer) if answer else 0)
        lf.flush()

        return jsonify({'response': answer, 'trace_id': trace_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', port=4000, debug=debug_mode)