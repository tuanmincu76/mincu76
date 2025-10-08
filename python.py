import streamlit as st
from google import genai
from google.genai.errors import APIError
import os # Dùng để lấy API key từ biến môi trường

# --- Cấu hình API và Mô hình ---
# Lấy API key từ biến môi trường 'GEMINI_API_KEY'.
# Đây là cách an toàn nhất khi triển khai (deployment).
api_key = os.getenv("GEMINI_API_KEY")

# Tên mô hình khuyến nghị cho tác vụ chat
MODEL_NAME = "gemini-2.5-flash"

# --- Khởi tạo Client và Chat Session ---

# Kiểm tra API Key và khởi tạo client
if not api_key:
    # Dừng ứng dụng và hiển thị lỗi nếu không tìm thấy key
    st.error("Lỗi: Không tìm thấy GEMINI_API_KEY trong biến môi trường. Vui lòng thiết lập để sử dụng Gemini.")
    client = None
else:
    try:
        # Khởi tạo client của Gemini
        client = genai.Client(api_key=api_key)

        # 1. Khởi tạo session state cho lịch sử tin nhắn hiển thị
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # 2. Khởi tạo session state cho đối tượng Chat Session (giữ bộ nhớ)
        if "chat_session" not in st.session_state:
            # Tạo một phiên chat mới
            st.session_state.chat_session = client.chats.create(model=MODEL_NAME)
            
    except APIError as e:
        st.error(f"Lỗi API khi khởi tạo: {e}. Vui lòng kiểm tra lại API Key.")
        client = None
    except Exception as e:
        st.error(f"Lỗi không xác định khi khởi tạo Gemini: {e}")
        client = None

# --- Tiêu đề và Nội dung Ứng dụng Hiện tại ---

st.title("Ứng dụng Streamlit với Chatbox Gemini 🤖💬")

# Giả định đây là phần mã cũ của bạn - Giữ nguyên các đoạn mã này
st.header("Phần nội dung chính hiện tại")
st.write("Các thành phần UI cũ của bạn (biểu đồ, bảng, metric, v.v.) sẽ nằm ở đây và hoạt động bình thường.")
st.metric(label="Một chỉ số giữ nguyên", value=1024, delta=25)
# Bạn có thể thêm bất kỳ đoạn mã hiện có nào của mình vào khu vực này.

# ----------------------------------------------------------------------
# 🌟 KHUNG CHAT ĐƯỢC THÊM VÀO 🌟
# ----------------------------------------------------------------------

st.markdown("---") # Đường kẻ ngang phân tách
st.subheader("Trò chuyện cùng Gemini (Model: gemini-2.5-flash) 🧠")

# Chỉ hiển thị và xử lý chat nếu client được khởi tạo thành công
if client and "chat_session" in st.session_state:
    
    # 1. Hiển thị lịch sử tin nhắn đã lưu trữ
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 2. Xử lý đầu vào từ người dùng
    if prompt := st.chat_input("Hỏi Gemini bất cứ điều gì..."):
        
        # Thêm tin nhắn của người dùng vào lịch sử hiển thị
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Hiển thị tin nhắn người dùng ngay lập tức
        with st.chat_message("user"):
            st.markdown(prompt)

        # 3. Gọi API Gemini và xử lý phản hồi
        with st.chat_message("assistant"):
            with st.spinner("Gemini đang suy nghĩ..."):
                try:
                    # Gửi tin nhắn đến chat session để duy trì lịch sử trò chuyện
                    response = st.session_session.chat_session.send_message(prompt)
                    
                    # Hiển thị phản hồi từ Gemini
                    st.markdown(response.text)
                    
                    # Thêm phản hồi của Gemini vào lịch sử hiển thị
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
                except APIError as e:
                    st.error(f"Lỗi API khi gửi tin nhắn: {e}")
                except Exception as e:
                    st.error(f"Lỗi không xác định trong quá trình giao tiếp: {e}")

# ----------------------------------------------------------------------
