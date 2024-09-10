import streamlit as st
import pymysql
import json


# 定义保存数据到 MySQL 的函数
def save_to_mysql(age, gender, location, selected_features, feature_scores, car_needs):
    try:
        # 连接到 MySQL 数据库
        conn = pymysql.connect(
            host="rm-2ze51s440w5h4957mao.mysql.rds.aliyuncs.com",
            port=3306,
            user="HDK1840",
            password="Hdk184018401840",
            database="app_use",
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        # 插入数据到表中
        query = """
        INSERT INTO survey_results (age, gender, location, important_features, feature_scores, car_needs)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            age,
            gender,
            location,
            ', '.join(selected_features),  # 将选中的特征转为字符串
            json.dumps(feature_scores, ensure_ascii=False),  # 将需求度分值字典转为 JSON 格式
            ', '.join(car_needs)  # 将用车需求转为字符串
        ))

        conn.commit()  # 提交事务
        cursor.close()
        conn.close()
        st.success("问卷结果已成功保存到数据库中！")

    except pymysql.MySQLError as err:
        st.error(f"数据库错误：{err}")


def main():
    st.title("新能源汽车需求调查问卷")

    # 基本信息
    st.header("1. 基本信息")
    age = st.number_input("1.1 年龄：", min_value=0, max_value=100, step=1)

    gender = st.radio("1.2 性别：", ('男', '女'))

    location = st.text_input("1.3 居住地：省市区（县）", "例如：北京市海淀区")

    # 新能源汽车特征需求调查
    st.header("2. 新能源汽车特征需求调查")

    st.subheader("2.1 请在以下7项新能源汽车产品特征中选出对您而言最重要几项（至多3项）")
    features = ["空间", "电池续航", "外观", "内饰", "驾驶体验", "智能化", "性价比"]
    selected_features = st.multiselect("选择最重要的特征（最多3项）", features, max_selections=3)

    st.subheader("2.2 请给出您对以下7项新能源汽车产品特征的需求度")
    st.write(
        "您给出的需求度分值越高，则证明该项特征对您而言越重要。每项特征能给出的需求度分值最大为10，且总分值不能超过35分。")

    # 初始化字典来保存每个特征的需求度分值
    feature_scores = {}
    total_score = 0

    for feature in features:
        score = st.slider(f"{feature} 的需求度分值：", 0, 10, 0)
        feature_scores[feature] = score
        total_score += score

    # 检查总分是否超过35
    if total_score > 35:
        st.error(f"总分值不能超过35分。您目前的总分值为 {total_score} 分，请调整。")

    # 用车需求调查
    st.header("3. 用车需求调查")

    st.subheader("3.1 请在以下13项新能源汽车用车需求中选出对您而言最重要几项（至多5项）")
    car_needs_options = [
        "上下班", "购物", "接送小孩", "自驾游", "跑长途",
        "商务差旅", "越野", "约会", "赛车", "拉货",
        "网约车", "组车队", "改装玩车"
    ]
    car_needs = st.multiselect("选择最重要的用车需求（最多5项）", car_needs_options, max_selections=5)

    # 提交按钮
    if st.button("提交"):
        if total_score <= 35:
            st.success("您的问卷已提交！")
            st.write("### 您的回答：")
            st.write(f"年龄：{age}")
            st.write(f"性别：{gender}")
            st.write(f"居住地：{location}")
            st.write("选择的最重要特征：", selected_features)
            st.write("需求度分值：", feature_scores)
            st.write("用车需求：", car_needs)

            # 保存数据到 MySQL
            save_to_mysql(age, gender, location, selected_features, feature_scores, car_needs)
        else:
            st.error("请确保需求度分值的总分不超过35分再提交。")


if __name__ == "__main__":
    main()
