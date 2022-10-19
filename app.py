import streamlit as st 
from PIL import Image
from main import get_book_names

file = st.file_uploader("Upload an image", type=["jpg", "jpeg"])

if file is not None:
    image = Image.open(file)

    st.image(
        image,
        caption=f"You amazing image has shape",
        use_column_width=True,
    )


    book_details = get_book_names(file)
    for book in book_details:
        image_col, text = st.columns([1,3])
        with image_col:
            if book['image_url'] != 'NA':
                st.image(book['image_url'], use_column_width = True)
            
        with text:
            st.write('Title : '+ book['title'])
            st.write('Author : '+ book['author'])
            st.write('Published Date : '+ book['publish_date'])