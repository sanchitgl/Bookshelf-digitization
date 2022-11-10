import streamlit as st 
from PIL import Image
from main import get_book_names

st.title("Book shelf Digitization")
file = st.file_uploader("Upload your Bookshelf image", type=["jpg", "jpeg", "png"])

if file is not None:
    image = Image.open(file)
    
    
    placeholder = st.empty()

    with placeholder.container():
        st.image(
                image,
                use_column_width=True
            )

    book_details = get_book_names(file)
    canny_im = Image.open("images_run/canny_edge.png")
    hough_im = Image.open("images_run/houghline.png")
    placeholder.empty()
    tab1, tab2, tab3 = st.tabs(["Input Image", "Canny-edge detection", "Houghline transformation"])
    with tab1:
        st.image(
            image,
            use_column_width=True,
        )
    with tab2:
        st.image(
            canny_im,
            use_column_width=True,
        )
    with tab3:
        st.image(
            hough_im,
            use_column_width=True,
        )

    for book in book_details:
        image_col, text = st.columns([1,3])
        with image_col:
            if book['image_url'] != 'NA':
                st.image(book['image_url'], use_column_width = True)
            
        with text:
            st.write('Title : '+ book['title'])
            st.write('Author : '+ book['author'])
            st.write('Published Date : '+ book['publish_date'])