class Group():
    def __init__(self, owner, isGhost, dbLocation):
        self.owner = owner
        self.isGhost = isGhost
        self.participants = [owner]
        self.TextChatRooms = []
        self.VoiceChatRooms = []
        self.db_location = dbLocation
        self.admins = [owner]

    def add_participants(self, adder, participant):
        if participant in self.participants:
            return 'participant already inside'
        if adder in self.admins:
            self.participants.append(participant)
            return 'participant added'
        return "don't have permission"

    def add_admin(self, adder, participant):
        if participant in self.admins:
            return 'participant already admin'
        if adder == self.owner:
            self.admins.append(participant)
            return 'admin set'
        return "don't have permission"

    def remove_participant(self, remover, participant):
        if participant in self.admins:
            if remover == self.owner:
                self.admins.remove(participant)
                self.participants.remove(participant)
                return "removed"
            else:
                return "don't have permission"
        if remover in self.admins:
            if not (participant in self.admins):
                return "removed"
        return "don't have permission"

    def remove_admin(self, remover, participant):
        if remover == self.owner:
            self.admins.remove(participant)
            return "removed"
        return "don't have permission"

    def add_text_message(self, participant, message):
        self.db_location