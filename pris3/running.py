import subprocess
import os

def process_command(command):
    command = command.strip().lower()
    
    if command == "obtain facial expressions":
        cmd = [
            "python", "pris3/inference/inference_audio2motion.py",
            "--a2m_ckpt", "pretrained_models/audio2motion/240210_real3dportrait_orig/audio2secc_vae",
            "--hubert_path", "pretrained_models/audio2motion/hubert",
            "--drv_aud", "pris3/demo/xinwen_5s.mp3",
            "--seed", "0",
            "--result_dir", "pris3/results/a2m",
            "--exp_file", "xinwen_5s.npy"
        ]
        try:
            subprocess.run(cmd, check=True)
            print("----------facial expressions obtained----------")
        except subprocess.CalledProcessError as e:
            print("Error occurred while obtaining facial expressions:", e)
    
    elif command == "render depth map":
        cmd = [
            "python", "-u", "pris3/inference/inference_edit_expression.py",
            "--name", "face_recon_feat0.2_augment",
            "--epoch=20",
            "--use_opengl", "False",
            "--checkpoints_dir", "pretrained_models",
            "--bfm_folder", "pretrained_models/BFM",
            "--infer_video_path", "pris3/demo/example_5s.mp4",
            "--infer_exp_coeff_path", "pris3/results/a2m/xinwen_5s.npy",
            "--infer_result_dir", "pris3/results/edit_expression"
        ]
        try:
            subprocess.run(cmd, check=True)
            print("----------depth map rendered----------")
        except subprocess.CalledProcessError as e:
            print("Error occurred while rendering depth map:", e)
    
    elif command == "generate facial animation":
        cmd = [
            "python", "-u", "pris3/inference/inference_joygen.py",
            "--unet_model_path", "pretrained_models/joygen",
            "--vae_model_path", "pretrained_models/sd-vae-ft-mse",
            "--intermediate_dir", "pris3/results/edit_expression",
            "--audio_path", "pris3/demo/xinwen_5s.mp3",
            "--video_path", "pris3/demo/example_5s.mp4",
            "--enable_pose_driven",
            "--result_dir", "pris3/results/talk",
            "--img_size", "256",
            "--gpu_id", "0"
        ]
        env = os.environ.copy()
        env["CUDA_VISIBLE_DEVICES"] = "0"
        try:
            subprocess.run(cmd, env=env, check=True)
            print("----------facial animation generated----------")
            print("results have stored as pris3/results/talk/example_5s#xinwen_5s.mp4")
        except subprocess.CalledProcessError as e:
            print("Error occurred while generating facial animation:", e)
        
    
    else:
        print("Unknown command. Please try again.")

if __name__ == '__main__':
    # 如果直接运行 demo.py，从标准输入获取命令
    user_input = input("Please enter a command: ")
    process_command(user_input)
