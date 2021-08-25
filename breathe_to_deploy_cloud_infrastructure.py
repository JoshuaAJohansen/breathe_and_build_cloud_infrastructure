import face_recognition
import cv2
from mouth_open_algorithm import get_lip_height, get_mouth_height


def is_mouth_open(face_landmarks):
    """
    Returns true if mouth is open, or false if it is not.
    """
    top_lip = face_landmarks['top_lip']
    top_lip_height = get_lip_height(top_lip)
    bottom_lip = face_landmarks['bottom_lip']
    bottom_lip_height = get_lip_height(bottom_lip)
    mouth_height = get_mouth_height(top_lip, bottom_lip)
    ratio = 0.5
    
    print(face_landmarks)
    print('top_lip_height: %.2f, bottom_lip_height: %.2f, mouth_height: %.2f, min*ratio: %.2f' 
        % (top_lip_height,bottom_lip_height,mouth_height, min(top_lip_height, bottom_lip_height) * ratio))

    # if mouth is open more than lip height * ratio, return true.
    if mouth_height > min(top_lip_height, bottom_lip_height) * ratio:
        return True
    else:
        return False


def breathe_and_run_code(function_to_run):
    total_breaths = 6
    breath_count = 0
    mouth_was_closed = True
    
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object to save video to local
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # codec
    # cv2.VideoWriter(filename, fourcc, fps, frameSize)
    out = cv2.VideoWriter('output.avi', fourcc, 7, (640, 480))

    # Load a sample picture and learn how to recognize it.
    josh_image = face_recognition.load_image_file("josh.jpg") # replace josh.jpg with your own image
    josh_face_encoding = face_recognition.face_encodings(josh_image)[0]
    while breath_count < total_breaths:

        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Find all the faces and face encodings in the frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_landmarks_list = face_recognition.face_landmarks(frame)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding, face_landmarks in zip(face_locations, face_encodings, face_landmarks_list):

            #  See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([josh_face_encoding], face_encoding)

            name = "Unknown"
            if match[0]:
                name = "Josh"

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom), (right, bottom + 35), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            # Display name on label
            cv2.putText(frame, name, (left + 6, bottom + 25), font, 1.0, (255, 255, 255), 1)
            
            # Check mouth alternated from open(exhale through) to closed(inhale through nose), 
            ret_mouth_open = is_mouth_open(face_landmarks)
            if ret_mouth_open is True:
                text = 'Mouth is open'
                if mouth_was_closed:
                    breath_count += 1
                    mouth_was_closed = False
            else:
                text = 'Open your mouth'
                mouth_was_closed = True
            cv2.putText(frame, text, (left, top - 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, f"Breath number: {str(breath_count)}", (left, top - 150), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
            print(f"Breath number: {str(breath_count)}")

        # Display the resulting image
        cv2.imshow('Video', frame)
        out.write(frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit(0)

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    # run
    function_to_run()


def deploy_app_using_terraform():
    """
    Initialize a terraform repository, generate a plan of what resources to provision, and applies the plan creating the cloud infrastructure. 
    
    Using the flag -auto-approve is useful when using an automation pipeline where user cannot pass in input.
    """
    print("")
    print("Running code:")
    print("")
    print("terraform init -input=false")
    print("terraform apply -input=false -auto-approve")

if __name__ == '__main__':
    breathe_and_run_code(deploy_app_using_terraform)

