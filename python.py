import streamlit as st
from google import genai
from google.genai.errors import APIError
import os # Dùng để lấy API key từ biến môi trường

# --- Cấu hình API và Mô hình ---
# Lấy API key từ biến môi trường. Rất quan trọng cho bảo mật!
# Đảm bảo bạn đã đặt biến môi trường tên là 'GEMINI_API_KEY'
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Lỗi: Không tìm thấy GEMINI_API_KEY trong biến môi trường. Vui lòng thiết lập!")
else:
    try:
        # Khởi tạo client của Gemini
        client = genai.Client(api_key=api_key)
        
        # Chọn mô hình phù hợp cho tác vụ chat
        MODEL_NAME = "gemini-2.5-flash"
        
        # --- Thiết lập Chat Session (Quan trọng cho việc duy trì lịch sử) ---
        # Kiểm tra xem 'chat' session đã tồn tại trong st.session_state chưa
        # Nếu chưa, tạo một session chat mới
        if "chat" not in st.session_state:
            try:
                # Khởi tạo một phiên chat (chat session) mới
                st.session_state.chat = client.chats.create(model=MODEL_NAME)
                st.session_state.messages = [] # Lưu trữ lịch sử tin nhắn cho hiển thị
                
            except APIError as e:
                st.error(f"Lỗi khởi tạo chat session với Gemini: {e}")
                st.session_state.chat = None # Đảm bảo không gọi chat nếu có lỗi
                
            except Exception as e:
                st.error(f"Lỗi không xác định khi khởi tạo chat session: {e}")
                st.session_state.chat = None
                
    except Exception as e:
        st.error(f"Lỗi khởi tạo Gemini Client: {e}")
        client = None # Đảm bảo không gọi client nếu có lỗi

# --- Giao diện Streamlit (Giữ nguyên các đoạn mã khác, thêm khung chat) ---

st.title("Ứng dụng Streamlit với Chatbox Gemini 🤖💬")

# Giả định đây là phần mã cũ của bạn
st.write("Đây là phần ứng dụng Streamlit hiện có của bạn.")
st.metric(label="Một chỉ số", value=42, delta=-1.4)
# Thêm bất kỳ thành phần Streamlit nào khác bạn muốn giữ lại ở đây...

# ----------------------------------------------------------------------
# 🌟 KHUNG CHAT MỚI ĐƯỢC THÊM VÀO 🌟
# ----------------------------------------------------------------------

st.markdown("---") # Đường kẻ ngang phân tách

if st.session_state.get("chat") and client:
    st.subheader("Trò chuyện cùng Gemini 🧠")
    
    # 1. Hiển thị lịch sử tin nhắn đã lưu trữ
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 2. Xử lý đầu vào từ người dùng (User Input)
    if prompt := st.chat_input("Hỏi Gemini bất cứ điều gì..."):
        # Thêm tin nhắn của người dùng vào lịch sử hiển thị
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Hiển thị tin nhắn người dùng
        with st.chat_message("user"):
            st.markdown(prompt)

        # 3. Gọi API Gemini và xử lý phản hồi
        with st.chat_message("assistant"):
            with st.spinner("Gemini đang suy nghĩ..."):
                try:
                    # Gửi tin nhắn đến chat session và lấy phản hồi
                    response = st.session_state.chat.send_message(prompt)
                    
                    # Hiển thị phản hồi từ Gemini
                    st.markdown(response.text)
                    
                    # Thêm phản hồi của Gemini vào lịch sử hiển thị
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
                except APIError as e:
                    st.error(f"Lỗi API khi gửi tin nhắn: {e}")
                    st.session_state.messages.pop() # Xóa tin nhắn người dùng để tránh kẹt
                except Exception as e:
                    st.error(f"Lỗi không xác định: {e}")
                    st.session_state.messages.pop()
                    
else:
    # Thông báo nếu không thể khởi tạo chat
    st.info("Không thể khởi tạo khung chat. Vui lòng kiểm tra API Key và kết nối.")
