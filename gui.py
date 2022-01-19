import streamlit as st
import requests
from pyDes import *
import base64
des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0" , pad=None, padmode=PAD_PKCS5)
base_url = 'http://h.saavncdn.com'
pentry="""#<unknown> - {}
C:\\Users\\monish\\Music{}.mp3"""
st.set_page_config(page_title="Music")

def play_music(url):
    audio_tag="""
    <audio controls>

  <source src="horse.m4a" type="audio/m4a-latm">
Your browser does not support the audio element.
</audio>
    """.format(url)

    st.markdown(audio_tag,unsafe_allow_html=True)
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
.stApp {
  background-image: url("data:image/png;base64,%s");
  background-size: cover;
}
</style>

    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def decrypt_url(url):
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url,padmode=PAD_PKCS5).decode('utf-8')
    dec_url = base_url + dec_url.replace('mp3:audios','')

    return dec_url[21:]


def search_song(a):

        lis=a.split(" ")
        string=""
        for i in lis:
            string=string+i+"+"

        search="https://www.jiosaavn.com/api.php?p=1&q={}&_format=json&_marker=0&api_version=4&ctx=wap6dot0&n=20&__call=search.getResults" .format(string)
        r=requests.get(search)
        dic=r.json()

        results=dic["results"]

        st.markdown("""<hr size="5" color="green"> """,unsafe_allow_html=True)
        for i in range (len(results)):

            cont=st.container()
            col1,col2,col3,col4=cont.columns(4)

            col1.image(results[i]["image"])
            col2.write(results[i]["title"])
            col2.write(results[i]["subtitle"])

            col3.markdown(""" <a href="{}" download="{}"  target="_blank" class="et_pb_button"><button type="button">Download</button></a>""" .format(decrypt_url(results[i]["more_info"]["encrypted_media_url"]),results[i]["subtitle"]),unsafe_allow_html=True)


            st.markdown("""<hr size="5" color="green"> """,unsafe_allow_html=True)



set_png_as_page_bg('im1.png')
st.title("Music Downloader")
st.markdown("""<hr size="5" color="green"> """,unsafe_allow_html=True)
st.subheader("Enter song name: ")


song_name=st.text_input("","Type here.....")

if(st.button("Search")):
    search_song(song_name)
