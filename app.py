import streamlit as st
import re
from datetime import date

from ai import analyze_food
from database import (
    create_table,
    add_meal,
    get_today_meals,
    get_meal_history,
    get_weekly_meals
)

st.set_page_config(
    page_title="MacroSnap - AI Nutrition Buddy",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 MacroSnap")
st.caption("Your AI nutrition buddy tracking made simple")


create_table()


def extract_number(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return float(match.group(1))

    return 0


# -----------------------------
# GOALS
# -----------------------------

if "calorie_goal" not in st.session_state:
    st.session_state.calorie_goal = 2500

if "protein_goal" not in st.session_state:
    st.session_state.protein_goal = 100

if "carbs_goal" not in st.session_state:
    st.session_state.carbs_goal = 300

if "fat_goal" not in st.session_state:
    st.session_state.fat_goal = 70


with st.expander("🎯 Set Your Daily Goals"):

    st.session_state.calorie_goal = st.number_input(
        "🔥 Calories",
        min_value=500,
        max_value=10000,
        value=st.session_state.calorie_goal,
        step=50
    )

    st.session_state.protein_goal = st.number_input(
        "💪 Protein (g)",
        min_value=10,
        max_value=500,
        value=st.session_state.protein_goal,
        step=5
    )

    st.session_state.carbs_goal = st.number_input(
        "🍚 Carbs (g)",
        min_value=10,
        max_value=1000,
        value=st.session_state.carbs_goal,
        step=5
    )

    st.session_state.fat_goal = st.number_input(
        "🥑 Fat (g)",
        min_value=10,
        max_value=500,
        value=st.session_state.fat_goal,
        step=5
    )


# -----------------------------
# TODAY'S DATA
# -----------------------------

today_meals = get_today_meals()

total_calories = sum(meal[0] for meal in today_meals)
total_protein = sum(meal[1] for meal in today_meals)
total_carbs = sum(meal[2] for meal in today_meals)
total_fat = sum(meal[3] for meal in today_meals)

# -----------------------------
# TODAY'S MEALS
# -----------------------------
st.divider()

st.subheader("🍽️ Today's Meals")

today_meal_history = [
    meal for meal in get_meal_history()
    if meal[0] == str(date.today())
]

if today_meal_history:
    for meal in today_meal_history:
        meal_date, meal_name, calories, protein, carbs, fat = meal

        meal_name = meal_name or "Meal"

        st.markdown(
    f"🍽️ **{meal_name}**  ·  🔥 **{int(calories)} kcal**"
)
else:
    st.info("No meals added today yet.")

# -----------------------------
# TODAY'S NUTRITION
# -----------------------------

st.subheader("📊 Today's Nutrition")


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔥 Calories",
        f"{int(total_calories)} / {int(st.session_state.calorie_goal)}"
    )

with col2:
    st.metric(
        "🥩 Protein",
        f"{int(total_protein)} / {int(st.session_state.protein_goal)} g"
    )

with col3:
    st.metric(
        "🍚 Carbs",
        f"{int(total_carbs)} / {int(st.session_state.carbs_goal)} g"
    )

with col4:
    st.metric(
        "🥑 Fat",
        f"{int(total_fat)} / {int(st.session_state.fat_goal)} g"
    )
    # -----------------------------
# GOAL PROGRESS
# -----------------------------

st.subheader("🎯 Goal Progress")

calorie_progress = min(
    total_calories / st.session_state.calorie_goal, 1.0
)

protein_progress = min(
    total_protein / st.session_state.protein_goal, 1.0
)

carbs_progress = min(
    total_carbs / st.session_state.carbs_goal, 1.0
)

fat_progress = min(
    total_fat / st.session_state.fat_goal, 1.0
)

st.write("🔥 Calories")
st.progress(calorie_progress)

st.write("🥩 Protein")
st.progress(protein_progress)

st.write("🍚 Carbs")
st.progress(carbs_progress)

st.write("🥑 Fat")
st.progress(fat_progress)
# -----------------------------
# ANALYZE MEAL
# -----------------------------

st.subheader("🍽️ Analyze a Meal")
st.caption("Upload a food photo or describe your meal to estimate calories and macros.")

meal_name = st.text_input(
    "🏷️ Meal name",
    placeholder="Example: Eggs and oats",
    max_chars=50,
    help="Give your meal a short name so you can identify it later in your meal history."
)

uploaded_image = st.file_uploader(
    "📸 Upload a food photo",
    type=["jpg", "jpeg", "png"],
    help="Upload a clear photo of your meal for AI analysis.",
    key="meal_photo"
)

food = st.text_area(
    "✍️ Or describe your meal",
    placeholder="Example: 4 eggs, 2 bananas and a bowl of oats",
    help="Include food quantities when possible, such as 4 eggs, 2 rotis, or 1 cup rice."
)

if st.button("🔍 Analyze Meal", use_container_width=True):

    if uploaded_image:
        result = analyze_food(image=uploaded_image)

    elif food.strip():
        result = analyze_food(text=food)

    else:
        st.warning("Please upload a food photo or describe your meal.")
        result = None

    if result:
        st.subheader("🤖 AI Analysis")
        st.caption("Estimated nutrition based on your meal description or photo.")
        st.info(result)

        calories = extract_number(
            r"(?:calories|total calories)[^0-9]*([0-9]+)",
            result
        )

        protein = extract_number(
            r"protein[^0-9]*([0-9]+)",
            result
        )

        carbs = extract_number(
            r"carbs?[^0-9]*([0-9]+)",
            result
        )

        fat = extract_number(
            r"fat[^0-9]*([0-9]+)",
            result
        )

        if calories > 0:

            if not meal_name:
                meal_name = "Meal"

            add_meal(
                meal_name,
                calories,
                protein,
                carbs,
                fat
            )

            st.success("✅ Meal added to your tracker!")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("🔥 Calories", f"{int(calories)} kcal")

            with col2:
                st.metric("🥩 Protein", f"{int(protein)} g")

            with col3:
                st.metric("🍚 Carbs", f"{int(carbs)} g")

            with col4:
                st.metric("🥑 Fat", f"{int(fat)} g")

        else:
            st.warning(
                "Could not extract nutrition values from the AI response."
            )
# -----------------------------
# MEAL HISTORY
# -----------------------------

st.subheader("📅 Meal History")

meal_history = get_meal_history()

if meal_history:
    current_date = None
    daily_calories = 0
    daily_protein = 0
    daily_carbs = 0
    daily_fat = 0

    for meal in meal_history:
        meal_date, meal_name, calories, protein, carbs, fat = meal
        meal_name = meal_name or "Meal"

        if current_date != meal_date:

            if current_date is not None:
                st.write(
                    f"**Daily Total:** "
                    
                    f"🔥 {int(daily_calories)} kcal | "
                    f"🥩 {int(daily_protein)}g protein | "
                    f"🍚 {int(daily_carbs)}g carbs | "
                    f"🥑 {int(daily_fat)}g fat"
                )
                st.divider()

            current_date = meal_date
            daily_calories = 0
            daily_protein = 0
            daily_carbs = 0
            daily_fat = 0

            st.markdown(f"### 📅 {meal_date}")

        daily_calories += calories
        daily_protein += protein
        daily_carbs += carbs
        daily_fat += fat

        st.write(
             f"🍽️ **{meal_name}** | "
             f"🔥 {int(calories)} kcal | "
             f"🥩 {int(protein)}g | "
             f"🍚 {int(carbs)}g | "
             f"🥑 {int(fat)}g"
    )

    st.write(
        f"**Daily Total:** "
        f"🔥 {int(daily_calories)} kcal | "
        f"🥩 {int(daily_protein)}g protein | "
        f"🍚 {int(daily_carbs)}g carbs | "
        f"🥑 {int(daily_fat)}g fat"
    )

else:
    st.info("No meal history yet.")
# -----------------------------
# WEEKLY SUMMARY
# -----------------------------

st.subheader("📈 Last 7 Days")

weekly_meals = get_weekly_meals()

if weekly_meals:
    weekly_calories = sum(meal[1] for meal in weekly_meals)
    weekly_protein = sum(meal[2] for meal in weekly_meals)

    days = len(set(meal[0] for meal in weekly_meals))

    average_calories = weekly_calories / days
    average_protein = weekly_protein / days

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🔥 Total Calories",
            f"{int(weekly_calories)} kcal"
        )

    with col2:
        st.metric(
            "📊 Avg Calories/Day",
            f"{int(average_calories)} kcal"
        )

    with col3:
        st.metric(
            "🥩 Avg Protein/Day",
            f"{int(average_protein)} g"
        )

    with col4:
        st.metric(
            "🍽️ Meals",
            len(weekly_meals)
        )

else:
    st.info("No meals recorded in the last 7 days.")
    # -----------------------------
# CALORIES CHART
# -----------------------------

st.subheader("🔥 Calories by Day")

if weekly_meals:

    daily_calories = {}

    for meal in weekly_meals:
        meal_date = meal[0]
        calories = meal[1]

        if meal_date not in daily_calories:
            daily_calories[meal_date] = 0

        daily_calories[meal_date] += calories

    chart_data = {
        "Date": list(daily_calories.keys()),
        "Calories": list(daily_calories.values())
    }

    st.bar_chart(
        chart_data,
        x="Date",
        y="Calories"
    )

else:
    st.info("No calorie data available yet.")
    # -----------------------------
# PROTEIN CHART
# -----------------------------

st.subheader("🥩 Protein by Day")

if weekly_meals:

    daily_protein = {}

    for meal in weekly_meals:
        meal_date = meal[0]
        protein = meal[2]

        if meal_date not in daily_protein:
            daily_protein[meal_date] = 0

        daily_protein[meal_date] += protein

    protein_chart_data = {
        "Date": list(daily_protein.keys()),
        "Protein": list(daily_protein.values())
    }

    st.bar_chart(
        protein_chart_data,
        x="Date",
        y="Protein"
    )

else:
    st.info("No protein data available yet.")
    # -----------------------------
# CARBS CHART
# -----------------------------

st.subheader("🍚 Carbs by Day")

if weekly_meals:

    daily_carbs = {}

    for meal in weekly_meals:
        meal_date = meal[0]
        carbs = meal[3]

        if meal_date not in daily_carbs:
            daily_carbs[meal_date] = 0

        daily_carbs[meal_date] += carbs

    carbs_chart_data = {
        "Date": list(daily_carbs.keys()),
        "Carbs": list(daily_carbs.values())
    }

    st.bar_chart(
        carbs_chart_data,
        x="Date",
        y="Carbs"
    )

else:
    st.info("No carbs data available yet.")
    # -----------------------------
# FAT CHART
# -----------------------------

st.subheader("🥑 Fat by Day")

if weekly_meals:

    daily_fat = {}

    for meal in weekly_meals:
        meal_date = meal[0]
        fat = meal[4]

        if meal_date not in daily_fat:
            daily_fat[meal_date] = 0

        daily_fat[meal_date] += fat

    fat_chart_data = {
        "Date": list(daily_fat.keys()),
        "Fat": list(daily_fat.values())
    }

    st.bar_chart(
        fat_chart_data,
        x="Date",
        y="Fat"
    )

else:
    st.info("No fat data available yet.")
    st.divider()
st.caption("🥗 MacroSnap • AI Nutrition Buddy")