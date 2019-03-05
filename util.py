import room as roomDef
import constants as const


def roombfs(px, py, gx, gy, room) -> int:
	toSearch = []

	explored = []
	for y in range(const.ROOM_HEIGHT):
		explored.append([])
		for x in range(const.ROOM_WIDTH):
			explored[y].append(False)

	pos = (0, px, py)

	if pos[2] - 1 >= 0 and room.monsters[(pos[1], pos[2] - 1)] is None and room.body[pos[2] - 1][pos[1]] not in roomDef.BLOCKING:
		toSearch.append((0, pos[1], pos[2] - 1))  # North

	if pos[1] + 1 < const.ROOM_WIDTH and room.monsters[(pos[1] + 1, pos[2])] is None and room.body[pos[2]][pos[1] + 1] not in roomDef.BLOCKING:
		toSearch.append((2, pos[1] + 1, pos[2]))  # East

	if pos[2] + 1 < const.ROOM_HEIGHT and room.monsters[(pos[1], pos[2] + 1)] is None and room.body[pos[2] + 1][pos[1]] not in roomDef.BLOCKING:
		toSearch.append((4, pos[1], pos[2] + 1))  # South

	if pos[1] - 1 >= 0 and room.monsters[(pos[1] - 1, pos[2])] is None and room.body[pos[2]][pos[1] - 1] not in roomDef.BLOCKING:
		toSearch.append((6, pos[1] - 1, pos[2]))  # West

	if pos[2] - 1 >= 0 and pos[1] + 1 < const.ROOM_WIDTH and room.monsters[(pos[1] + 1, pos[2] - 1)] is None and room.body[pos[2] - 1][pos[1] + 1] not in roomDef.BLOCKING and room.body[pos[2]][pos[1] + 1] not in roomDef.BLOCKING and room.body[pos[2] - 1][pos[1]] not in roomDef.BLOCKING:
		toSearch.append((1, pos[1] + 1, pos[2] - 1))  # North-East

	if pos[2] + 1 < const.ROOM_HEIGHT and pos[1] + 1 < const.ROOM_WIDTH and room.monsters[(pos[1] + 1, pos[2] + 1)] is None and room.body[pos[2] + 1][pos[1] + 1] not in roomDef.BLOCKING and room.body[pos[2] - 1][pos[1]] not in roomDef.BLOCKING and room.body[pos[2]][pos[1] + 1] not in roomDef.BLOCKING:
		toSearch.append((3, pos[1] + 1, pos[2] + 1))  # South-East

	if pos[2] + 1 < const.ROOM_HEIGHT and pos[1] - 1 >= 0 and room.monsters[(pos[1] - 1, pos[2] + 1)] is None and room.body[pos[2] + 1][pos[1] - 1] not in roomDef.BLOCKING and room.body[pos[2]][pos[1] - 1] not in roomDef.BLOCKING and room.body[pos[2] - 1][pos[1]] not in roomDef.BLOCKING:
		toSearch.append((5, pos[1] - 1, pos[2] + 1))  # South-West

	if pos[1] - 1 >= 0 and pos[2] - 1 >= 0 and room.monsters[(pos[1] - 1, pos[2] - 1)] is None and room.body[pos[2] - 1][pos[1] - 1] not in roomDef.BLOCKING and room.body[pos[2] - 1][pos[1]] not in roomDef.BLOCKING and room.body[pos[2]][pos[1] - 1] not in roomDef.BLOCKING:
		toSearch.append((7, pos[1] - 1, pos[2] - 1))  # North-West

	while len(toSearch) > 0:
		pos = toSearch.pop(0)
		if pos[1] == gx and pos[2] == gy:
			return pos[0]

		if (not ((0 <= pos[1] < const.ROOM_WIDTH) and (0 <= pos[2] < const.ROOM_HEIGHT))) or explored[pos[2]][pos[1]]:
			continue

		explored[pos[2]][pos[1]] = True

		if pos[2] - 1 >= 0 and room.body[pos[2] - 1][pos[1]] not in roomDef.BLOCKING:
			toSearch.append((pos[0], pos[1], pos[2] - 1)) # North

		if pos[1] + 1 < const.ROOM_WIDTH and room.body[pos[2]][pos[1] + 1] not in roomDef.BLOCKING:
			toSearch.append((pos[0], pos[1] + 1, pos[2])) # East

		if pos[2] + 1 < const.ROOM_HEIGHT and room.body[pos[2] + 1][pos[1]] not in roomDef.BLOCKING:
			toSearch.append((pos[0], pos[1], pos[2] + 1)) # South

		if pos[1] - 1 >= 0 and room.body[pos[2]][pos[1] - 1] not in roomDef.BLOCKING:
			toSearch.append((pos[0], pos[1] - 1, pos[2])) # West

		if pos[1] + 1 < const.ROOM_WIDTH and pos[2] - 1 >= 0 and room.body[pos[2] - 1][pos[1] + 1] not in roomDef.BLOCKING and room.body[pos[2] - 1][pos[1]] not in roomDef.BLOCKING and room.body[pos[2]][pos[1] + 1] not in roomDef.BLOCKING:
			toSearch.append((pos[0], pos[1] + 1, pos[2] - 1)) # North-East

		if pos[2] + 1 < const.ROOM_HEIGHT and pos[1] + 1 < const.ROOM_WIDTH and room.body[pos[2] + 1][pos[1] + 1] not in roomDef.BLOCKING and room.body[pos[2]][pos[1] + 1] not in roomDef.BLOCKING and room.body[pos[2] + 1][pos[1]] not in roomDef.BLOCKING:
			toSearch.append((pos[0], pos[1] + 1, pos[2] + 1)) # South-East

		if pos[1] - 1 >= 0 and pos[2] + 1 < const.ROOM_HEIGHT and room.body[pos[2] + 1][pos[1] - 1] not in roomDef.BLOCKING and room.body[pos[2] + 1][pos[1]] not in roomDef.BLOCKING and room.body[pos[2]][pos[1] - 1] not in roomDef.BLOCKING:
			toSearch.append((pos[0], pos[1] - 1, pos[2] + 1)) # South-West

		if pos[1] - 1 >= 0 and pos[2] - 1 > 0 and room.body[pos[2] - 1][pos[1] - 1] not in roomDef.BLOCKING and room.body[pos[2]][pos[1] - 1] not in roomDef.BLOCKING and room.body[pos[2] - 1][pos[1]] not in roomDef.BLOCKING:
			toSearch.append((pos[0], pos[1] - 1, pos[2] - 1)) # North-West

	return -1
