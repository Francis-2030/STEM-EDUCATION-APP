# modules/pyopengl_renderer.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class OpenGLRenderer:
    def __init__(self, window_id):
        self.window_id = window_id
        self.angle = 0
        self.initialized = False
    
    def init_gl(self):
        """Initialize OpenGL context"""
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(800, 600)
        glutCreateWindow("Robotics Simulator")
        
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.2, 1.0)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 800/600, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        self.initialized = True
    
    def draw_robot(self):
        """Draw a simple robot model"""
        glLoadIdentity()
        gluLookAt(0, 2, 5, 0, 0, 0, 0, 1, 0)
        
        glRotatef(self.angle, 0, 1, 0)
        
        # Body
        glColor3f(0.8, 0.2, 0.2)
        glutSolidCube(1.0)
        
        # Head
        glPushMatrix()
        glTranslatef(0, 0.8, 0)
        glColor3f(0.2, 0.2, 0.8)
        glutSolidSphere(0.3, 20, 20)
        glPopMatrix()
        
        # Arms
        arm_angle = math.sin(self.angle * 0.05) * 30
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 0.6, 0, 0)
            glRotatef(arm_angle, 1, 0, 0)
            glScalef(0.2, 0.2, 1.0)
            glColor3f(0.2, 0.8, 0.2)
            glutSolidCube(1.0)
            glPopMatrix()
    
    def display(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_robot()
        glutSwapBuffers()
    
    def animate(self):
        """Update animation"""
        self.angle = (self.angle + 0.5) % 360
        glutPostRedisplay()
    
    def start(self):
        """Start the main loop"""
        if not self.initialized:
            self.init_gl()
        
        glutDisplayFunc(self.display)
        glutIdleFunc(self.animate)
        glutMainLoop()
    
    def reset(self):
        """Reset animation state"""
        self.angle = 0