import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")

#+++++++++++++++++++++++++++++++++++++++++ uploading file and preprocessing +++++++++++++++++++++++++++++++++++++++++++++++
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #+++++++++++++++++++++++++++++++++++++++=+++++ fetch unique users ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    #++++++++++++++++++++++++++++++++++++++++++ Stats of Selected User ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if st.sidebar.button("Show Analysis"):
        result = helper.fetch_stats(selected_user, df)

        if result:
            num_messages, words, num_media_messages, num_links = result
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(num_links)
        else:
            st.write("Error: No data returned from `fetch_stats`.")


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++ TIMELINE +++++++++++++++++++++++++++++++++++++++++++++++++++++++
        st.title("Timelines")
        col1, col2 = st.columns(2)

        with col1:
            #monthly
            st.header("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
                    #daily
            st.header("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='violet')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++ ACTIVITY MAP ++++++++++++++++++++++++++++++++++++++++++++++++++++++
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++ MOST BUSY USER ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if selected_user == "Overall":
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='blue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        #++++++++++++++++++++++++++++++++++++++++++++++++++++++ MOST COMMON WORDS +++++++++++++++++++++++++++++++++++++++++++++++
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation = "vertical")

        st.title("Most Common Words")
        st.pyplot(fig)
        
        #wordcloud of the most common words 
        st.title("Word Cloud of Most Words")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')

        st.pyplot(fig)


        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++ EMOJI ANALYSIS +++++++++++++++++++++++++++++++++++++++++++++++++
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            # ax.bar(emoji_df[0], emoji_df[1])
            st.pyplot(fig)

