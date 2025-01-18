from kafka import KafkaConsumer, TopicPartition
import json


# consumerB starting the 
consumer1 = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='consumer-group-1',
    auto_offset_reset='earliest',
)
topic = "sectionABC"
partition = 1
topic_with_partition = TopicPartition(topic, partition)
consumer1.assign([topic_with_partition])


PASS_MARKS = 300

# Initialize counters
total_students = 0
students_passed = 0
students_failed = []

print("Processing messages...")

try:
    for message in consumer1:
        student = json.loads(message.value.decode('utf-8'))
        #print(student)
        if student['section'] == 'C':
            total_students += 1

            total_marks = (student['english'] +  student['math'] +student['physics'] + student['chemistry'] + student['biology'])
            if total_marks >= PASS_MARKS:
                students_passed += 1
            else:
                students_failed.append({
                    "name": student["name"],
                    "total_marks": total_marks
                })

        # Break after processing 100 messages for this example
        if total_students >= 100:
            break

except KeyboardInterrupt:
    print("\nConsumer interrupted. Exiting...")

finally:
    consumer1.close()

# Calculate pass percentage
if total_students > 0:
    pass_percentage = (students_passed / total_students) * 100
    print(f"\nTotal students in section C: {total_students}")
    print(f"Students passed: {students_passed}")
    print(f"Pass percentage: {pass_percentage:.2f}%")
    print("\nStudents who failed:")

    for failed_student in students_failed:
        print(f"- {failed_student['name']} (Total Marks: {failed_student['total_marks']})")
else:
    print("No students from section C were found.")