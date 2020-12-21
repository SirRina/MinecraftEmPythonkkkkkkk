from api.libs import pygame, GL, GLU;
from api.util import Vec, lerp, clamp;
from math     import sin, cos, sqrt, degrees, radians, pi;

class Camera:
	MOUSE_SENSIVITY = 0.1;
	MOUSE_INVERTED  = False;

	CAMERA_LENGHT = 0.2;

	def __init__(self, main, debug):
		self.position = Vec(0, 0, 0);

		self.yaw   = 60;
		self.pitch = 0;

		self.debug   = debug;
		self.focused = False;

		self.main = main;

		self.x, self.y, self.z = 0, 0, 0;

	def get_pos(self):
		return self.position.get();

	def set_pos(self, x, y, z):
		self.position.x, self.position.y, self.position.z = x, y, z;

	def get_yaw_pitch(self):
		return [self.yaw, self.pitch];

	def set_yaw(self, amount):
		self.yaw -= amount;

	def set_pitch(self, amount):
		if self.MOUSE_INVERTED:
			self.pitch -= amount;
		else:
			self.pitch += amount

	def calcule_x_from_angle(self, angle):
		return sin(radians(angle));

	def calcule_z_from_angle(self, angle):
		return cos(radians(angle));

	def focus(self):
		self.focused = True;

	def set_pos(self, x, y, z):
		self.position.x = x;
		self.position.y = y;
		self.position.z = z;

	def set_static_pos(self, x, y, z):
		self.set_pos(x, y, z);

		self.x = x;
		self.y = y;
		self.z = z;

	def update_camera(self, delta_time, w, h):
		GL.glLoadIdentity();

		keys = pygame.key.get_pressed();
		rel  = pygame.mouse.get_rel();

		forward_speed  = 0.5 * delta_time;
		backward_speed = 0.4 * delta_time;

		strafe_speed = 0.4 * delta_time;

		if self.focused:
			if keys[pygame.K_w]:
				self.position.x += self.calcule_x_from_angle(self.yaw) * forward_speed;
				self.position.z += self.calcule_z_from_angle(self.yaw) * forward_speed;

			if keys[pygame.K_s]:
				self.position.x -= self.calcule_x_from_angle(self.yaw) * backward_speed;
				self.position.z -= self.calcule_z_from_angle(self.yaw) * backward_speed;

			if keys[pygame.K_a]:
				self.position.x -= strafe_speed * self.calcule_x_from_angle(self.yaw - 90);
				self.position.z -= strafe_speed * self.calcule_z_from_angle(self.yaw - 90);

			if keys[pygame.K_d]:
				self.position.x += strafe_speed * self.calcule_x_from_angle(self.yaw - 90);
				self.position.z += strafe_speed * self.calcule_z_from_angle(self.yaw - 90);

			if keys[pygame.K_SPACE]:
				self.position.y -= 0.1;

			if keys[pygame.K_LSHIFT]:
				self.position.y += 0.1;

			self.set_yaw(  (rel[0]) * self.MOUSE_SENSIVITY);
			self.set_pitch((rel[1]) * self.MOUSE_SENSIVITY);

		pygame.event.set_grab(self.focused)
		pygame.mouse.set_visible(self.focused != True);

		if self.debug:
			print(self.position.get());

		if self.pitch >= 90:
			self.pitch = 90;

		if self.pitch <= -90:
			self.pitch = -90;

		GL.glRotate(self.pitch, 1, 0, 0)
		GL.glRotate(360 - self.yaw, 0, 1, 0);

		# el ogro
		self.x = lerp(self.x, self.position.x, self.main.partial_ticks);
		self.y = lerp(self.y, self.position.y, self.main.partial_ticks);
		self.z = lerp(self.z, self.position.z, self.main.partial_ticks);

		GL.glTranslate(self.x, self.y, self.z);