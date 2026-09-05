import json
from pathlib import Path
import cv2
import numpy as np

class FaceEngine:
    def __init__(self):
        self.app=None
        self.error=None
        try:
            from insightface.app import FaceAnalysis
            self.app=FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
            self.app.prepare(ctx_id=0, det_size=(640,640))
        except Exception as e:
            self.error=str(e)

    def embedding_from_bytes(self, data: bytes):
        image=cv2.imdecode(np.frombuffer(data,np.uint8), cv2.IMREAD_COLOR)
        if image is None: raise ValueError('Invalid image')
        return self.embedding_from_image(image)

    def embedding_from_image(self, image):
        if self.app is None: raise RuntimeError(f'Face engine unavailable: {self.error}')
        faces=self.app.get(image)
        if not faces: raise ValueError('No face detected')
        # For registration, use the largest face.
        face=max(faces,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
        emb=face.normed_embedding.astype(float).tolist()
        return emb

    def recognize(self, data: bytes, known, threshold=0.42):
        image=cv2.imdecode(np.frombuffer(data,np.uint8), cv2.IMREAD_COLOR)
        if image is None: raise ValueError('Invalid image')
        if self.app is None: raise RuntimeError(f'Face engine unavailable: {self.error}')
        faces=self.app.get(image)
        results=[]
        for face in faces:
            emb=face.normed_embedding
            best=None
            for student, stored in known:
                score=float(np.dot(emb, np.array(stored)))
                if best is None or score>best[0]: best=(score,student)
            if best and best[0]>=threshold:
                results.append({'student_id':best[1].id,'name':best[1].name,'register_number':best[1].register_number,'confidence':best[0]})
            else:
                results.append({'student_id':None,'name':'Unknown','register_number':None,'confidence':best[0] if best else 0.0})
        return results
