export default function EmployeesList({ employees }) {
  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">Employees</h3>
      <ul className="grid grid-cols-2 gap-2">
        {employees.map((emp, index) => (
          <li
            key={index}
            className="border rounded p-2 bg-gray-50"
          >
            <p className="font-medium">{emp.name}</p>
            <p className="text-sm text-gray-600">{emp.role}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
